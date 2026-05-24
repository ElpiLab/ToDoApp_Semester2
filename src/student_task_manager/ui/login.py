from nicegui import ui, app
from student_task_manager.services.auth_service import AuthService

auth_service = AuthService()


def login_page():
    ui.colors(primary="#1B5E20")

    def try_login():
        try:
            user = auth_service.login(email.value or "", password.value or "")
        except ValueError as e:
            ui.notify(str(e), color="negative")
            return

        if user:
            app.storage.user.update(
                {
                    "authenticated": True,
                    "user_id": user.id,
                    "email": user.email,
                    "full_name": user.full_name,
                }
            )
            ui.navigate.to("/")
        else:
            ui.notify("Invalid email or password", color="negative")

    with ui.card().classes("absolute-center w-96 p-6"):
        ui.label("Welcome Back").classes("text-h5 font-bold mb-6 text-center")

        email = ui.input("Email").props("outlined").classes("w-full mb-3")
        password = ui.input("Password", password=True).props("outlined").classes("w-full mb-4")

        password.on("keydown.enter", try_login)

        ui.button("Login", on_click=try_login).props("color=green-9 unelevated").classes(
            "w-full mb-3"
        )

        ui.separator().classes("my-4")

        with ui.row().classes("w-full justify-center gap-2"):
            ui.label("Don't have an account?").classes("text-sm text-slate-600")
            ui.link("Register here", "/register").classes("text-sm font-semibold text-emerald-700")


def register_login_route() -> None:
    ui.page("/login")(login_page)
