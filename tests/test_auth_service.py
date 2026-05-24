import pytest
from passlib.hash import bcrypt
from sqlmodel import Session

from student_task_manager.domain.models import Student
from student_task_manager.services.auth_service import (
    AuthService,
    DuplicateEmailError,
    LoginThrottle,
)


def session_factory(engine):
    return lambda: Session(engine)


def test_change_password_updates_hash(seeded_test_engine):
    svc = AuthService(session_factory(seeded_test_engine))
    with Session(seeded_test_engine) as session:
        user = session.get(Student, 1)
        user.password_hash = bcrypt.hash("oldpass")
        session.add(user)
        session.commit()

    svc.change_password(1, "oldpass", "newpass123")

    with Session(seeded_test_engine) as session:
        user = session.get(Student, 1)
        assert bcrypt.verify("newpass123", user.password_hash)
        assert not bcrypt.verify("oldpass", user.password_hash)


def test_change_password_rejects_wrong_current(seeded_test_engine):
    svc = AuthService(session_factory(seeded_test_engine))
    with Session(seeded_test_engine) as session:
        user = session.get(Student, 1)
        user.password_hash = bcrypt.hash("oldpass")
        session.add(user)
        session.commit()

    with pytest.raises(ValueError, match="Current password is incorrect"):
        svc.change_password(1, "wrong", "newpass123")

    with Session(seeded_test_engine) as session:
        user = session.get(Student, 1)
        assert bcrypt.verify("oldpass", user.password_hash)


def test_change_password_rejects_short_new_password(seeded_test_engine):
    svc = AuthService(session_factory(seeded_test_engine))
    with Session(seeded_test_engine) as session:
        user = session.get(Student, 1)
        user.password_hash = bcrypt.hash("oldpass")
        session.add(user)
        session.commit()

    with pytest.raises(ValueError, match="New password must be at least 10 characters"):
        svc.change_password(1, "oldpass", "short")

    with Session(seeded_test_engine) as session:
        user = session.get(Student, 1)
        assert bcrypt.verify("oldpass", user.password_hash)


def test_change_password_rejects_long_new_password(seeded_test_engine):
    svc = AuthService(session_factory(seeded_test_engine))
    with Session(seeded_test_engine) as session:
        user = session.get(Student, 1)
        user.password_hash = bcrypt.hash("oldpass")
        session.add(user)
        session.commit()

    with pytest.raises(ValueError, match="New password must be at most 72 bytes"):
        svc.change_password(1, "oldpass", "x" * 73)

    with Session(seeded_test_engine) as session:
        user = session.get(Student, 1)
        assert bcrypt.verify("oldpass", user.password_hash)


def test_change_password_rejects_reusing_current_password(seeded_test_engine):
    svc = AuthService(session_factory(seeded_test_engine))
    with Session(seeded_test_engine) as session:
        user = session.get(Student, 1)
        user.password_hash = bcrypt.hash("oldpassword123")
        session.add(user)
        session.commit()

    with pytest.raises(ValueError, match="New password must differ from the current one"):
        svc.change_password(1, "oldpassword123", "oldpassword123")

    with Session(seeded_test_engine) as session:
        user = session.get(Student, 1)
        assert bcrypt.verify("oldpassword123", user.password_hash)


def test_update_profile_rejects_missing_user(seeded_test_engine) -> None:
    svc = AuthService(session_factory(seeded_test_engine))

    with pytest.raises(ValueError, match="User not found"):
        svc.update_profile(999, "Missing User", "missing@example.com")


@pytest.mark.parametrize(
    ("full_name", "email", "message"),
    [
        ("", "student@example.com", "Name cannot be empty"),
        ("Test Student", "not-an-email", "Enter a valid email address"),
    ],
)
def test_update_profile_validates_input(
    seeded_test_engine,
    full_name: str,
    email: str,
    message: str,
) -> None:
    svc = AuthService(session_factory(seeded_test_engine))

    with pytest.raises(ValueError, match=message):
        svc.update_profile(1, full_name, email)


def test_update_profile_updates_name_without_current_password(seeded_test_engine) -> None:
    svc = AuthService(session_factory(seeded_test_engine))

    user = svc.update_profile(1, "  Updated Student  ", "student@example.com")

    assert user.full_name == "Updated Student"
    assert user.email == "student@example.com"


def test_update_profile_requires_current_password_for_email_change(seeded_test_engine) -> None:
    svc = AuthService(session_factory(seeded_test_engine))

    with pytest.raises(ValueError, match="Current password is required to change email"):
        svc.update_profile(1, "Test Student", "new-email@example.com")


def test_update_profile_rejects_wrong_current_password_for_email_change(
    seeded_test_engine,
) -> None:
    svc = AuthService(session_factory(seeded_test_engine))
    with Session(seeded_test_engine) as session:
        user = session.get(Student, 1)
        user.password_hash = bcrypt.hash("oldpass")
        session.add(user)
        session.commit()

    with pytest.raises(ValueError, match="Current password is incorrect"):
        svc.update_profile(
            1,
            "Test Student",
            "new-email@example.com",
            current_password="wrongpass",
        )


def test_update_profile_rejects_duplicate_email_change(seeded_test_engine) -> None:
    svc = AuthService(session_factory(seeded_test_engine))
    with Session(seeded_test_engine) as session:
        user = session.get(Student, 1)
        user.password_hash = bcrypt.hash("oldpass")
        session.add(user)
        session.commit()

    with pytest.raises(ValueError, match="Email already in use"):
        svc.update_profile(
            1,
            "Test Student",
            "other@example.com",
            current_password="oldpass",
        )


def test_update_profile_normalizes_email_case(seeded_test_engine) -> None:
    svc = AuthService(session_factory(seeded_test_engine))
    with Session(seeded_test_engine) as session:
        user = session.get(Student, 1)
        user.password_hash = bcrypt.hash("oldpass")
        session.add(user)
        session.commit()

    user = svc.update_profile(
        1,
        "Test Student",
        "  MIXED.CASE@Example.COM  ",
        current_password="oldpass",
    )

    assert user.email == "mixed.case@example.com"


def test_register_creates_normalized_user(seeded_test_engine) -> None:
    svc = AuthService(session_factory(seeded_test_engine))

    user = svc.register(
        "  New Student  ",
        "  NEW@Example.COM  ",
        "secret1234",
        "secret1234",
    )

    assert user.id is not None
    assert user.full_name == "New Student"
    assert user.email == "new@example.com"
    assert bcrypt.verify("secret1234", user.password_hash)


@pytest.mark.parametrize(
    ("full_name", "email", "password", "confirm_password", "message"),
    [
        ("", "new@example.com", "secret1234", "secret1234", "Name cannot be empty"),
        (
            "New Student",
            "not-an-email",
            "secret1234",
            "secret1234",
            "Enter a valid email address",
        ),
        ("New Student", "new@example.com", "secret1234", "different", "Passwords do not match"),
        (
            "New Student",
            "new@example.com",
            "short",
            "short",
            "Password must be at least 10 characters",
        ),
        (
            "New Student",
            "new@example.com",
            "x" * 73,
            "x" * 73,
            "Password must be at most 72 bytes",
        ),
    ],
)
def test_register_validates_input(
    seeded_test_engine,
    full_name: str,
    email: str,
    password: str,
    confirm_password: str,
    message: str,
) -> None:
    svc = AuthService(session_factory(seeded_test_engine))

    with pytest.raises(ValueError, match=message):
        svc.register(full_name, email, password, confirm_password)


def test_register_rejects_duplicate_email(
    seeded_test_engine, caplog: pytest.LogCaptureFixture
) -> None:
    svc = AuthService(session_factory(seeded_test_engine))

    caplog.set_level("WARNING", logger="student_task_manager.services.auth_service")
    with pytest.raises(DuplicateEmailError, match="Unable to create account with those details"):
        svc.register(
            "Test Student",
            "student@example.com",
            "secret1234",
            "secret1234",
        )

    assert "Registration rejected because email already exists" in caplog.text
    assert "student@example.com" not in caplog.text


def test_duplicate_registration_does_not_replace_existing_password(seeded_test_engine) -> None:
    svc = AuthService(session_factory(seeded_test_engine))
    with Session(seeded_test_engine) as session:
        user = session.get(Student, 1)
        user.password_hash = bcrypt.hash("original123")
        session.add(user)
        session.commit()

    with pytest.raises(DuplicateEmailError):
        svc.register(
            "Test Student",
            "student@example.com",
            "replacement123",
            "replacement123",
        )

    assert svc.login("student@example.com", "replacement123") is None
    assert svc.login("student@example.com", "original123") is not None


def test_login_rejects_empty_credentials(seeded_test_engine) -> None:
    svc = AuthService(session_factory(seeded_test_engine))

    with pytest.raises(ValueError, match="Email and password are required"):
        svc.login("", "")


def test_login_normalizes_email_case(seeded_test_engine) -> None:
    svc = AuthService(session_factory(seeded_test_engine))
    with Session(seeded_test_engine) as session:
        user = session.get(Student, 1)
        user.password_hash = bcrypt.hash("oldpass")
        session.add(user)
        session.commit()

    logged_in = svc.login("  STUDENT@Example.COM  ", "oldpass")

    assert logged_in is not None
    assert logged_in.id == 1


def test_login_returns_none_for_malformed_stored_hash(seeded_test_engine) -> None:
    svc = AuthService(session_factory(seeded_test_engine))
    with Session(seeded_test_engine) as session:
        user = session.get(Student, 1)
        user.password_hash = "not-a-valid-hash"
        session.add(user)
        session.commit()

    assert svc.login("student@example.com", "oldpass") is None


def test_login_throttles_repeated_failed_attempts(seeded_test_engine) -> None:
    now = 100.0
    throttle = LoginThrottle(now=lambda: now, max_failures=2, lockout_seconds=30)
    svc = AuthService(session_factory(seeded_test_engine), login_throttle=throttle)
    with Session(seeded_test_engine) as session:
        user = session.get(Student, 1)
        user.password_hash = bcrypt.hash("oldpass")
        session.add(user)
        session.commit()

    assert svc.login("student@example.com", "wrong") is None
    assert svc.login("student@example.com", "wrong") is None
    with pytest.raises(ValueError, match="Too many login attempts"):
        svc.login("student@example.com", "oldpass")


def test_login_success_resets_throttle(seeded_test_engine) -> None:
    throttle = LoginThrottle(max_failures=2, lockout_seconds=30)
    svc = AuthService(session_factory(seeded_test_engine), login_throttle=throttle)
    with Session(seeded_test_engine) as session:
        user = session.get(Student, 1)
        user.password_hash = bcrypt.hash("oldpass")
        session.add(user)
        session.commit()

    assert svc.login("student@example.com", "wrong") is None
    assert svc.login("student@example.com", "oldpass") is not None
    assert svc.login("student@example.com", "wrong") is None
    assert svc.login("student@example.com", "oldpass") is not None
