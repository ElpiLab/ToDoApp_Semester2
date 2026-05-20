from datetime import date

from student_task_manager.domain.models import Priority, Status, Task
from student_task_manager.ui import controllers


def test_create_task_parses_due_date_and_notifies(monkeypatch) -> None:
    notifications = []

    class FakeService:
        def create_task(self, title, description, priority, due_date, category="Other"):
            assert title == "Task title"
            assert description == "Task description"
            assert priority == Priority.medium
            assert due_date == date(2026, 5, 12)
            return Task(id=1, title=title, description=description, priority=priority)

    monkeypatch.setattr(controllers, "service", FakeService())
    monkeypatch.setattr(
        controllers.ui,
        "notify",
        lambda message, type, **kwargs: notifications.append((message, type)),
    )

    task = controllers.create_task("Task title", "Task description", "medium", "2026-05-12")

    assert task is not None
    assert notifications == [('Task "Task title" created successfully', "positive")]


def test_update_task_uses_service_boundary(monkeypatch) -> None:
    notifications = []

    class FakeService:
        def update_task(self, task_id, **updates):
            assert task_id == 3
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

    monkeypatch.setattr(controllers, "service", FakeService())
    monkeypatch.setattr(
        controllers.ui,
        "notify",
        lambda message, type, **kwargs: notifications.append((message, type)),
    )

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
