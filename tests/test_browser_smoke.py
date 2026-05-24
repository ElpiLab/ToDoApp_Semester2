from concurrent.futures import ThreadPoolExecutor

import pytest
from nicegui import run
from nicegui.testing.user_simulation import user_simulation

from student_task_manager.ui.login import login_page
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
