from datetime import date

from nicegui import ui

from domain.models import Priority
from services.task_service import TaskService


service = TaskService()


def create_task(title: str, description: str, priority: str, due_date: str | None):
    try:
        parsed_due_date = date.fromisoformat(due_date) if due_date else None

        task = service.create_task(
            title=title,
            description=description,
            priority=Priority(priority),
            due_date=parsed_due_date,
        )
        ui.notify(f'Task "{task.title}" created successfully', type='positive')
    except Exception as e:
        ui.notify(str(e), type='negative')


def delete_task(task_id: int):
    try:
        service.delete_task(task_id)
        ui.notify("Task deleted", type='positive')
    except Exception as e:
        ui.notify(str(e), type='negative')


def complete_task(task_id: int):
    try:
        service.mark_complete(task_id)
        ui.notify("Task marked as complete", type='positive')
    except Exception as e:
        ui.notify(str(e), type='negative')


def get_tasks():
    return service.get_all_tasks()