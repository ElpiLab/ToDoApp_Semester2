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