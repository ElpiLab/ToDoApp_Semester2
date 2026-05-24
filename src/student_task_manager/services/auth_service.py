from collections.abc import Callable
from dataclasses import dataclass, field
import logging
from time import monotonic

from passlib.hash import bcrypt
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select
from student_task_manager.data_access.db import get_session
from student_task_manager.domain.models import Student
from student_task_manager.domain.validation import is_valid_email, normalize_email

MAX_BCRYPT_PASSWORD_BYTES = 72
MIN_PASSWORD_LENGTH = 10
MAX_LOGIN_FAILURES = 5
LOGIN_LOCKOUT_SECONDS = 60.0
logger = logging.getLogger(__name__)


class DuplicateEmailError(ValueError):
    """Raised when registration cannot use the requested email."""


def _validate_full_name(full_name: str) -> str:
    normalized_name = full_name.strip()
    if not normalized_name:
        raise ValueError("Name cannot be empty")
    return normalized_name


def _validate_email(email: str) -> str:
    normalized_email = normalize_email(email)
    if not is_valid_email(normalized_email):
        raise ValueError("Enter a valid email address")
    return normalized_email


def _validate_password_length(password: str, *, label: str = "Password") -> None:
    if len(password) < MIN_PASSWORD_LENGTH:
        raise ValueError(f"{label} must be at least {MIN_PASSWORD_LENGTH} characters")
    if len(password.encode("utf-8")) > MAX_BCRYPT_PASSWORD_BYTES:
        raise ValueError(f"{label} must be at most {MAX_BCRYPT_PASSWORD_BYTES} bytes")


@dataclass
class _LoginFailure:
    count: int = 0
    locked_until: float = 0.0


@dataclass
class LoginThrottle:
    now: Callable[[], float] = monotonic
    max_failures: int = MAX_LOGIN_FAILURES
    lockout_seconds: float = LOGIN_LOCKOUT_SECONDS
    _failures: dict[str, _LoginFailure] = field(default_factory=dict)

    def check_allowed(self, email: str) -> None:
        failure = self._failures.get(email)
        if failure is not None and failure.locked_until > self.now():
            raise ValueError("Too many login attempts. Try again later")

    def record_failure(self, email: str) -> None:
        failure = self._failures.setdefault(email, _LoginFailure())
        failure.count += 1
        if failure.count >= self.max_failures:
            failure.locked_until = self.now() + self.lockout_seconds

    def record_success(self, email: str) -> None:
        self._failures.pop(email, None)


class AuthService:
    def __init__(
        self,
        session_factory: Callable[[], Session] = get_session,
        login_throttle: LoginThrottle | None = None,
    ) -> None:
        self.session_factory = session_factory
        self.login_throttle = login_throttle or LoginThrottle()

    def login(self, email: str, password: str) -> Student | None:
        normalized_email = normalize_email(email)
        if not normalized_email or not password:
            raise ValueError("Email and password are required")
        self.login_throttle.check_allowed(normalized_email)

        with self.session_factory() as session:
            statement = select(Student).where(Student.email == normalized_email)
            user = session.exec(statement).first()
            if user is None:
                self.login_throttle.record_failure(normalized_email)
                return None
            try:
                password_matches = bcrypt.verify(password, user.password_hash)
            except ValueError:
                self.login_throttle.record_failure(normalized_email)
                return None
            if not password_matches:
                self.login_throttle.record_failure(normalized_email)
                return None
            self.login_throttle.record_success(normalized_email)
            return user

    def update_profile(
        self,
        user_id: int,
        full_name: str,
        email: str | None = None,
        current_password: str | None = None,
    ) -> Student:
        normalized_name = _validate_full_name(full_name)
        with self.session_factory() as session:
            user = session.get(Student, user_id)
            if not user:
                raise ValueError("User not found")
            user.full_name = normalized_name
            if email is not None:
                new_email = _validate_email(email)
                if new_email != user.email:
                    if not current_password:
                        raise ValueError("Current password is required to change email")
                    try:
                        password_matches = bcrypt.verify(current_password, user.password_hash)
                    except ValueError as exc:
                        raise ValueError("Current password is incorrect") from exc
                    if not password_matches:
                        raise ValueError("Current password is incorrect")
                    existing = session.exec(
                        select(Student).where(Student.email == new_email)
                    ).first()
                    if existing and existing.id != user_id:
                        raise ValueError("Email already in use")
                    user.email = new_email
            session.add(user)
            try:
                session.commit()
            except IntegrityError as exc:
                session.rollback()
                raise ValueError("Email already in use") from exc
            session.refresh(user)
            return user

    def register(
        self,
        full_name: str,
        email: str,
        password: str,
        confirm_password: str,
    ) -> Student:
        normalized_name = _validate_full_name(full_name)
        normalized_email = _validate_email(email)
        if password != confirm_password:
            raise ValueError("Passwords do not match")
        _validate_password_length(password)

        with self.session_factory() as session:
            existing = session.exec(
                select(Student).where(Student.email == normalized_email)
            ).first()
            if existing:
                logger.warning("Registration rejected because email already exists")
                raise DuplicateEmailError("Unable to create account with those details")

            user = Student(
                email=normalized_email,
                password_hash=bcrypt.hash(password),
                full_name=normalized_name,
            )
            session.add(user)
            try:
                session.commit()
            except IntegrityError as exc:
                session.rollback()
                logger.exception("Registration rejected because database integrity check failed")
                raise DuplicateEmailError("Unable to create account with those details") from exc
            session.refresh(user)
            return user

    def change_password(
        self,
        user_id: int,
        current_password: str,
        new_password: str,
    ) -> Student:
        with self.session_factory() as session:
            user = session.get(Student, user_id)
            if not user:
                raise ValueError("User not found")
            try:
                password_matches = bcrypt.verify(current_password, user.password_hash)
            except ValueError as exc:
                raise ValueError("Current password is incorrect") from exc
            if not password_matches:
                raise ValueError("Current password is incorrect")
            _validate_password_length(new_password, label="New password")
            if new_password == current_password:
                raise ValueError("New password must differ from the current one")
            user.password_hash = bcrypt.hash(new_password)
            session.add(user)
            session.commit()
            session.refresh(user)
            return user
