from datetime import date
from types import SimpleNamespace

import pytest

from student_task_manager.domain.models import Priority, Status, Task
from student_task_manager.ui import controllers


def test_create_task_parses_due_date_and_notifies(monkeypatch) -> None:
    notifications = []

    class FakeService:
        def create_task(self, title, description, priority, due_date, category="Other", *, user_id):
            assert title == "Task title"
            assert description == "Task description"
            assert priority == Priority.medium
            assert due_date == date(2026, 5, 12)
            assert category == "Other"
            assert user_id == 5
            return Task(id=1, title=title, description=description, priority=priority)

    def capture_notify(message, type, **kwargs) -> None:
        assert kwargs["position"] == "top-right"
        notifications.append((message, type))

    monkeypatch.setattr(controllers, "service", FakeService())
    monkeypatch.setattr(controllers, "_current_user_id", lambda: 5)
    monkeypatch.setattr(controllers.ui, "notify", capture_notify)

    task = controllers.create_task("Task title", "Task description", "medium", "2026-05-12")

    assert task is not None
    assert notifications == [('Task "Task title" created successfully', "positive")]


def test_update_task_uses_service_boundary(monkeypatch) -> None:
    notifications = []

    class FakeService:
        def update_task(self, task_id, user_id, **updates):
            assert task_id == 3
            assert user_id == 5
            assert updates["priority"] == Priority.high
            assert updates["status"] == Status.in_progress
            assert updates["due_date"] == date(2026, 5, 15)
            return Task(
                id=task_id,
                title=updates["title"],
                description=updates["description"],
                priority=updates["priority"],
                status=updates["status"],
                due_date=updates["due_date"],
            )

    def capture_notify(message, type, **kwargs) -> None:
        assert kwargs["position"] == "top-right"
        notifications.append((message, type))

    monkeypatch.setattr(controllers, "service", FakeService())
    monkeypatch.setattr(controllers, "_current_user_id", lambda: 5)
    monkeypatch.setattr(controllers.ui, "notify", capture_notify)

    task = controllers.update_task(
        3,
        "Revise notes",
        "Prepare for exam week",
        "high",
        "in_progress",
        "2026-05-15",
    )

    assert task is not None
    assert notifications == [('Task "Revise notes" updated successfully', "positive")]


def test_create_task_requires_logged_in_user(monkeypatch) -> None:
    notifications = []

    def capture_notify(message, type, **kwargs) -> None:
        assert kwargs["position"] == "top-right"
        notifications.append((message, type))

    monkeypatch.setattr(
        controllers,
        "_current_user_id",
        lambda: (_ for _ in ()).throw(ValueError("Login required")),
    )
    monkeypatch.setattr(controllers.ui, "notify", capture_notify)

    task = controllers.create_task("Task title", "Task description", "medium", "2026-05-12")

    assert task is None
    assert notifications == [("Login required", "negative")]


@pytest.mark.parametrize("stored_user_id", [True, False])
def test_current_user_id_rejects_boolean_session_values(monkeypatch, stored_user_id: bool) -> None:
    fake_app = SimpleNamespace(storage=SimpleNamespace(user={"user_id": stored_user_id}))
    monkeypatch.setattr(controllers, "app", fake_app)

    with pytest.raises(ValueError, match="Login required"):
        controllers._current_user_id()


def test_delete_all_tasks_uses_single_success_notification(monkeypatch) -> None:
    notifications = []

    class FakeService:
        def delete_all_tasks(self, *, user_id):
            assert user_id == 5
            return 3

    def capture_notify(message, type, **kwargs) -> None:
        assert kwargs["position"] == "top-right"
        notifications.append((message, type))

    monkeypatch.setattr(controllers, "service", FakeService())
    monkeypatch.setattr(controllers, "_current_user_id", lambda: 5)
    monkeypatch.setattr(controllers.ui, "notify", capture_notify)

    deleted_count = controllers.delete_all_tasks()

    assert deleted_count == 3
    assert notifications == [("Deleted 3 tasks", "positive")]


def test_create_task_reraises_unexpected_service_error(monkeypatch) -> None:
    notifications = []

    class BrokenService:
        def create_task(self, *args, **kwargs):
            assert args == ()
            assert kwargs["title"] == "Task title"
            assert kwargs["user_id"] == 5
            raise RuntimeError("database unavailable")

    def fail_notify(message, type, **kwargs) -> None:
        pytest.fail(f"Unexpected notification: {message} {type} {kwargs}")

    monkeypatch.setattr(controllers, "service", BrokenService())
    monkeypatch.setattr(controllers, "_current_user_id", lambda: 5)
    monkeypatch.setattr(controllers.ui, "notify", fail_notify)

    with pytest.raises(RuntimeError, match="database unavailable"):
        controllers.create_task("Task title", "Task description", "medium", "2026-05-12")

    assert notifications == []
