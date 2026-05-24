from concurrent.futures import ThreadPoolExecutor

import pytest
from nicegui import run
from nicegui.testing.user_simulation import user_simulation

from student_task_manager.services.auth_service import DuplicateEmailError
from student_task_manager.ui.login import login_page
from student_task_manager.ui import registration
from student_task_manager.ui.registration import register_page


@pytest.mark.anyio
async def test_simulated_browser_can_open_login_page(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(run, "ProcessPoolExecutor", ThreadPoolExecutor)

    async with user_simulation(root=login_page) as user:
        await user.open("/")

        user.find("Welcome Back")
        user.find("Register here")


@pytest.mark.anyio
async def test_simulated_browser_can_open_registration_page(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(run, "ProcessPoolExecutor", ThreadPoolExecutor)

    async with user_simulation(root=register_page) as user:
        await user.open("/")

        user.find("Create Account")
        user.find("Back to Login")


@pytest.mark.anyio
async def test_duplicate_registration_stays_on_registration_page(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class DuplicateAuthService:
        def register(self, full_name, email, password, confirm_password):
            raise DuplicateEmailError("Unable to create account with those details")

    monkeypatch.setattr(run, "ProcessPoolExecutor", ThreadPoolExecutor)
    monkeypatch.setattr(registration, "auth_service", DuplicateAuthService())

    async with user_simulation(root=register_page) as user:
        await user.open("/")
        user.find("Register").click()

        await user.should_see("Unable to create an account with those details")
        user.find("Create Account")
