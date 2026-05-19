from datetime import date
from nicegui import ui, app
from domain.models import Priority, Status
from services.task_service import TaskService

service = TaskService()


def get_current_user_id() -> int | None:
    """Get the current logged-in user's ID"""
    return app.storage.user.get('user_id')


def _parse_due_date(due_date: str | None) -> date | None:
    if not due_date:
        return None
    normalized = due_date.strip().replace(".", "-").replace("/", "-")
    return date.fromisoformat(normalized)


def create_task(title: str, description: str, priority: str, due_date: str | None):
    user_id = get_current_user_id()
    if not user_id:
        ui.notify('Please login first', type='warning', position='bottom')
        return None
    
    try:
        task = service.create_task(
            user_id=user_id,
            title=title,
            description=description,
            priority=Priority(priority),
            due_date=_parse_due_date(due_date),
        )
        ui.notify(f'Task "{task.title}" created successfully', type="positive", position="bottom")
        return task
    except Exception as e:
        ui.notify(str(e), type="negative", position="bottom")
        return None


def delete_task(task_id: int):
    user_id = get_current_user_id()
    if not user_id:
        return False
    
    try:
        service.delete_task(task_id, user_id)
        ui.notify("Task deleted", type="positive", position="bottom")
        return True
    except Exception as e:
        ui.notify(str(e), type="negative", position="bottom")
        return False


def complete_task(task_id: int):
    user_id = get_current_user_id()
    if not user_id:
        return False
    
    try:
        service.mark_complete(task_id, user_id)
        ui.notify("Task marked as complete", type="positive", position="bottom")
        return True
    except Exception as e:
        ui.notify(str(e), type="negative", position="bottom")
        return False


def mark_task_pending(task_id: int):
    user_id = get_current_user_id()
    if not user_id:
        return False
    
    try:
        service.mark_pending(task_id, user_id)
        ui.notify("Task moved back to pending", type="positive", position="bottom")
        return True
    except Exception as e:
        ui.notify(str(e), type="negative", position="bottom")
        return False


def change_task_status(task_id: int, target_status: str):
    user_id = get_current_user_id()
    if not user_id:
        return None
    
    try:
        updated_task = service.update_task(
            task_id, 
            user_id,
            status=Status(target_status)
        )
        return updated_task
    except Exception as e:
        ui.notify(str(e), type="negative", position="bottom")
        return None


def update_task(task_id: int, title: str, description: str, priority: str, status: str, due_date: str | None):
    user_id = get_current_user_id()
    if not user_id:
        return None
    
    try:
        updated_task = service.update_task(
            task_id,
            user_id,
            title=title,
            description=description,
            priority=Priority(priority),
            status=Status(status),
            due_date=_parse_due_date(due_date),
        )
        ui.notify(f'Task "{updated_task.title}" updated successfully', type="positive", position="bottom")
        return updated_task
    except Exception as e:
        ui.notify(str(e), type="negative", position="bottom")
        return None


def get_tasks():
    """Get tasks for current user only"""
    user_id = get_current_user_id()
    if not user_id:
        return []
    
    return service.get_user_tasks(user_id)