from nicegui import ui, app
from sqlmodel import Session
from data_access.db import engine
from services.auth_service import AuthService

auth_service = AuthService()


@ui.page('/login')
def login_page():

    def try_login():
        with Session(engine) as session:
            user = auth_service.login(
                session,
                email.value,
                password.value
            )

            if user:
                # Store authenticated user
                app.storage.user.update({
                    'authenticated': True,
                    'user_id': user.id,
                    'email': user.email,
                    'full_name': user.full_name,
                })
                ui.navigate.to('/')
            else:
                ui.notify('Invalid email or password', color='negative')

    # Absolute center - no column needed
    with ui.card().classes('absolute-center w-96 p-6'):
        ui.label('Welcome Back').classes('text-h5 font-bold mb-6 text-center')
        
        email = ui.input('Email').props('outlined').classes('w-full mb-3')
        password = ui.input('Password', password=True).props('outlined').classes('w-full mb-4')
        
        password.on('keydown.enter', try_login)
        
        ui.button('Login', on_click=try_login).props('color=teal-7 unelevated').classes('w-full mb-3')
        
        ui.separator().classes('my-4')
        
        with ui.row().classes('w-full justify-center gap-2'):
            ui.label("Don't have an account?").classes('text-sm text-slate-600')
            ui.link('Register here', '/register').classes('text-sm font-semibold text-teal-600')