from passlib.hash import bcrypt
from sqlmodel import Session, select
from domain.models import Student


class AuthService:

    def register(self, session: Session, name: str, email: str, password: str):
        hashed = bcrypt.hash(password)

        student = Student(
            name=name,
            email=email,
            password_hash=hashed,
            role='student'
        )

        session.add(student)
        session.commit()
        session.refresh(student)
        return student

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
                existing = session.exec(
                    select(Student).where(Student.email == new_email)
                ).first()
                if existing and existing.id != user_id:
                    raise ValueError("Email already in use")
                user.email = new_email
        session.add(user)
        session.commit()
        session.refresh(user)
        return user