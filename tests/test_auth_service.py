import pytest
from passlib.hash import bcrypt
from sqlmodel import Session

from student_task_manager.domain.models import Student
from student_task_manager.services.auth_service import AuthService


def test_change_password_updates_hash(seeded_test_engine):
    svc = AuthService()
    with Session(seeded_test_engine) as session:
        user = session.get(Student, 1)
        user.password_hash = bcrypt.hash("oldpass")
        session.add(user)
        session.commit()

    with Session(seeded_test_engine) as session:
        svc.change_password(session, 1, "oldpass", "newpass")

    with Session(seeded_test_engine) as session:
        user = session.get(Student, 1)
        assert bcrypt.verify("newpass", user.password_hash)
        assert not bcrypt.verify("oldpass", user.password_hash)


def test_change_password_rejects_wrong_current(seeded_test_engine):
    svc = AuthService()
    with Session(seeded_test_engine) as session:
        user = session.get(Student, 1)
        user.password_hash = bcrypt.hash("oldpass")
        session.add(user)
        session.commit()

    with Session(seeded_test_engine) as session:
        with pytest.raises(ValueError, match="Current password is incorrect"):
            svc.change_password(session, 1, "wrong", "newpass")

    with Session(seeded_test_engine) as session:
        user = session.get(Student, 1)
        assert bcrypt.verify("oldpass", user.password_hash)


def test_change_password_rejects_short_new_password(seeded_test_engine):
    svc = AuthService()
    with Session(seeded_test_engine) as session:
        user = session.get(Student, 1)
        user.password_hash = bcrypt.hash("oldpass")
        session.add(user)
        session.commit()

    with Session(seeded_test_engine) as session:
        with pytest.raises(ValueError, match="New password must be at least 6 characters"):
            svc.change_password(session, 1, "oldpass", "short")

    with Session(seeded_test_engine) as session:
        user = session.get(Student, 1)
        assert bcrypt.verify("oldpass", user.password_hash)


def test_change_password_rejects_reusing_current_password(seeded_test_engine):
    svc = AuthService()
    with Session(seeded_test_engine) as session:
        user = session.get(Student, 1)
        user.password_hash = bcrypt.hash("oldpass")
        session.add(user)
        session.commit()

    with Session(seeded_test_engine) as session:
        with pytest.raises(ValueError, match="New password must differ from the current one"):
            svc.change_password(session, 1, "oldpass", "oldpass")

    with Session(seeded_test_engine) as session:
        user = session.get(Student, 1)
        assert bcrypt.verify("oldpass", user.password_hash)
