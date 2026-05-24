from nicegui import ui
from student_task_manager.services.auth_service import AuthService, DuplicateEmailError

auth_service = AuthService()
REGISTRATION_RESULT_MESSAGE = "Account created. Please login."
DUPLICATE_REGISTRATION_MESSAGE = (
    "Unable to create an account with those details. "
    "Try logging in with the existing password or use a different email."
)


def register_page():
    ui.colors(primary="#1B5E20")

    def try_register():
        try:
            auth_service.register(
                full_name.value or "",
                email.value or "",
                password.value or "",
                confirm_password.value or "",
            )
        except DuplicateEmailError:
            ui.notify(DUPLICATE_REGISTRATION_MESSAGE, color="negative")
            return
        except ValueError as e:
            ui.notify(str(e), color="negative")
            return

        ui.notify(REGISTRATION_RESULT_MESSAGE, color="positive")
        ui.navigate.to("/login")

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


def register_registration_route() -> None:
    ui.page("/register")(register_page)
