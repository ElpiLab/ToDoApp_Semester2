import os
from collections.abc import Mapping

from nicegui import app, ui

from student_task_manager.data_access.db import (
    create_db_and_tables,
    database_url,
    safe_database_url_for_logs,
)
from student_task_manager.deployment import dev_admin_config, server_config, storage_secret
from student_task_manager.services.auth_service import AuthService, DuplicateEmailError
from student_task_manager.ui.login import register_login_route
from student_task_manager.ui.registration import register_registration_route
from student_task_manager.ui.routes import register_main_routes

app.add_static_files("/assets", "assets")


def create_dev_admin_if_enabled(env: Mapping[str, str] = os.environ) -> bool:
    config = dev_admin_config(env)
    if config is None:
        return False

    email, full_name, password = config
    try:
        AuthService().register(full_name, email, password, password)
    except DuplicateEmailError:
        print("Development admin already exists.")
        return False
    else:
        print(f"Development admin created for {email}.")
        return True


def run() -> None:
    print(f"Using database URL: {safe_database_url_for_logs(database_url())}")
    create_db_and_tables()
    create_dev_admin_if_enabled()
    register_login_route()
    register_registration_route()
    register_main_routes()

    host, port = server_config()
    ui.run(title="Bizzy", port=port, host=host, reload=False, storage_secret=storage_secret())


if __name__ == "__main__":
    run()
