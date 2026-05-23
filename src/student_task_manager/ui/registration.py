from nicegui import ui
from sqlmodel import Session
from passlib.hash import bcrypt
from student_task_manager.data_access.db import engine
from student_task_manager.domain.models import Student


@ui.page("/register")
def register_page():
    ui.colors(primary="#1B5E20")

    def try_register():
        # Validate passwords match
        if password.value != confirm_password.value:
            ui.notify("Passwords do not match!", color="negative")
            return

        # Validate password length
        if len(password.value) < 6:
            ui.notify("Password must be at least 6 characters", color="negative")
            return

        with Session(engine) as session:
            # Check if user already exists
            from sqlmodel import select

            existing = session.exec(select(Student).where(Student.email == email.value)).first()

            if existing:
                ui.notify("Email already registered!", color="negative")
                return

            # Create new user
            try:
                # Hash the password
                hashed_password = bcrypt.hash(password.value)

                new_user = Student(
                    email=email.value,
                    password_hash=hashed_password,
                    full_name=full_name.value,
                    is_active=True,
                )

                session.add(new_user)
                session.commit()

                ui.notify("Registration successful! Please login.", color="positive")
                ui.navigate.to("/login")

            except Exception as e:
                ui.notify(f"Error: {str(e)}", color="negative")
                session.rollback()

    with ui.card().classes("absolute-center w-96 p-6"):
        ui.label("Create Account").classes("text-h5 font-bold mb-4 text-center")

        full_name = ui.input("Full Name").props("outlined").classes("w-full mb-3")
        email = ui.input("Email").props("outlined type=email").classes("w-full mb-3")
        password = ui.input("Password", password=True).props("outlined").classes("w-full mb-3")
        confirm_password = (
            ui.input("Confirm Password", password=True).props("outlined").classes("w-full mb-4")
        )

        with ui.row().classes("w-full gap-3"):
            ui.button("Register", on_click=try_register).props("color=green-9 unelevated").classes(
                "flex-1"
            )
            ui.button("Back to Login", on_click=lambda: ui.navigate.to("/login")).props(
                "flat color=green-9"
            ).classes("flex-1")
