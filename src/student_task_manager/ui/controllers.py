from datetime import date

from nicegui import ui

from student_task_manager.domain.models import Priority, Status
from student_task_manager.services.task_service import TaskService


service = TaskService()


def _parse_due_date(due_date: str | None) -> date | None:
    if not due_date:
        return None
    normalized = due_date.strip().replace(".", "-").replace("/", "-")
    return date.fromisoformat(normalized)


def create_task(
    title: str,
    description: str,
    priority: str,
    due_date: str | None,
    category: str = "Other",
):
    try:
        task = service.create_task(
            title=title,
            description=description,
            priority=Priority(priority),
            due_date=_parse_due_date(due_date),
            category=category,
        )
        ui.notify(
            f'Task "{task.title}" created successfully', type="positive", position="top-right"
        )
        return task
    except Exception as e:
        ui.notify(str(e), type="negative", position="top-right")
        return None


def delete_task(task_id: int):
    try:
        service.delete_task(task_id)
        ui.notify("Task deleted", type="positive", position="top-right")
        return True
    except Exception as e:
        ui.notify(str(e), type="negative", position="top-right")
        return False


def complete_task(task_id: int):
    try:
        service.mark_complete(task_id)
        ui.notify("Task marked as complete", type="positive", position="top-right")
        return True
    except Exception as e:
        ui.notify(str(e), type="negative", position="top-right")
        return False


def mark_task_pending(task_id: int):
    try:
        service.mark_pending(task_id)
        ui.notify("Task moved back to pending", type="positive", position="top-right")
        return True
    except Exception as e:
        ui.notify(str(e), type="negative", position="top-right")
        return False


def change_task_status(task_id: int, target_status: str):
    try:
        updated_task = service.update_task(task_id, status=Status(target_status))
        return updated_task
    except Exception as e:
        ui.notify(str(e), type="negative", position="top-right")
        return None


def update_task(
    task_id: int,
    title: str,
    description: str,
    priority: str,
    status: str,
    due_date: str | None,
    category: str = "Other",
):
    try:
        updated_task = service.update_task(
            task_id,
            title=title,
            description=description,
            priority=Priority(priority),
            status=Status(status),
            due_date=_parse_due_date(due_date),
            category=category,
        )
        ui.notify(
            f'Task "{updated_task.title}" updated successfully',
            type="positive",
            position="top-right",
        )
        return updated_task
    except Exception as e:
        ui.notify(str(e), type="negative", position="top-right")
        return None


def get_tasks():
    return service.get_all_tasks()
