from passlib.hash import bcrypt
from sqlmodel import Session, select
from student_task_manager.domain.models import Student


class AuthService:
    def login(self, session: Session, email: str, password: str):
        statement = select(Student).where(Student.email == email)
        user = session.exec(statement).first()

        if user and bcrypt.verify(password, user.password_hash):
            return user

        return None

    def update_profile(
        self,
        session: Session,
        user_id: int,
        full_name: str,
        email: str | None = None,
    ):
        user = session.get(Student, user_id)
        if not user:
            return None
        user.full_name = full_name.strip()
        if email is not None:
            new_email = email.strip()
            if new_email != user.email:
                existing = session.exec(select(Student).where(Student.email == new_email)).first()
                if existing and existing.id != user_id:
                    raise ValueError("Email already in use")
                user.email = new_email
        session.add(user)
        session.commit()
        session.refresh(user)
        return user

    def change_password(
        self,
        session: Session,
        user_id: int,
        current_password: str,
        new_password: str,
    ):
        user = session.get(Student, user_id)
        if not user:
            raise ValueError("User not found")
        if not bcrypt.verify(current_password, user.password_hash):
            raise ValueError("Current password is incorrect")
        if len(new_password) < 6:
            raise ValueError("New password must be at least 6 characters")
        if new_password == current_password:
            raise ValueError("New password must differ from the current one")
        user.password_hash = bcrypt.hash(new_password)
        session.add(user)
        session.commit()
        session.refresh(user)
        return user
