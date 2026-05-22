from nicegui import ui
import os
from sqlmodel import Session, select
import bcrypt

from data_access.db import create_db_and_tables, engine
from domain.models import Student
import ui.pages as pages_module
import ui.login as login_module
import ui.registration as register_module


def hash_password(password: str) -> str:
    password_bytes = password.encode('utf-8')
    if len(password_bytes) > 72:
        password_bytes = password_bytes[:72]
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')


def create_default_user():
    try:
        with Session(engine) as session:
            existing_user = session.exec(select(Student)).first()
            if not existing_user:
                hashed_pw = hash_password("admin123")
                default_user = Student(
                    email="admin@example.com",
                    password_hash=hashed_pw,
                    full_name="Admin User",
                    is_active=True
                )
                session.add(default_user)
                session.commit()
                print("=" * 50)
                print("✅ Default user created: admin@example.com / admin123")
                print("=" * 50)
    except Exception as e:
        print(f"Error: {e}")


def run():
    create_db_and_tables()
    create_default_user()

    # port = int(os.environ.get("PORT", 8080))
    port = int(os.environ.get("PORT", 8081))  # use 8081 instead of 8080
    host = "0.0.0.0"
    secret = os.environ.get("STORAGE_SECRET", "dev-secret")

    print(f"Starting Bizzy on {host}:{port}")
    ui.run(
        title="Bizzy",
        port=port,
        host=host,
        reload=False,
        storage_secret=secret
    )


if __name__ == "__main__":
    run()