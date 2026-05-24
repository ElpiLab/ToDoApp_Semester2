import os

from nicegui import app, ui
from sqlmodel import Session, select
import bcrypt

from student_task_manager.data_access.db import create_db_and_tables, engine
from student_task_manager.deployment import server_config
from student_task_manager.domain.models import Student
import student_task_manager.ui.routes as routes_module  # noqa: F401
import student_task_manager.ui.login as login_module  # noqa: F401
import student_task_manager.ui.registration as register_module  # noqa: F401

app.add_static_files("/assets", "assets")


def hash_password(password: str) -> str:
    """Hash a password safely using bcrypt directly"""
    password_bytes = password.encode("utf-8")
    if len(password_bytes) > 72:
        password_bytes = password_bytes[:72]
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode("utf-8")


def create_default_user():
    """Create a default admin user if no users exist"""
    try:
        with Session(engine) as session:
            existing_user = session.exec(select(Student)).first()
            if not existing_user:
                hashed_pw = hash_password("admin123")
                default_user = Student(
                    email="admin@example.com",
                    password_hash=hashed_pw,
                    full_name="Admin User",
                    is_active=True,
                )
                session.add(default_user)
                session.commit()
                print("=" * 50)
                print("Default user created successfully.")
                print("Email: admin@example.com")
                print("Password: admin123")
                print("=" * 50)
                return True
            else:
                print("Users already exist.")
                return False
    except Exception as e:
        print(f"Error creating default user: {e}")
        return False


def run() -> None:
    create_db_and_tables()
    create_default_user()

    secret_key = os.environ.get("STORAGE_SECRET")
    if not secret_key:
        secret_key = "dev-secret-key-do-not-use-in-production"
        print("WARNING: Using development storage secret.")

    host, port = server_config()
    ui.run(title="Bizzy", port=port, host=host, reload=False, storage_secret=secret_key)


if __name__ == "__main__":
    run()
