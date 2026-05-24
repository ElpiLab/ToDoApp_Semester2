from datetime import date

from student_task_manager.data_access.dao import TaskDAO
from student_task_manager.domain.models import Priority, Status, Task


def _allowed_values(enum_type: type[Priority] | type[Status]) -> str:
    return ", ".join(item.value for item in enum_type)


def _coerce_priority(value: Priority | str | None) -> Priority:
    if value is None:
        raise ValueError("Priority is required")
    if isinstance(value, Priority):
        return value
    if isinstance(value, str):
        try:
            return Priority(value)
        except ValueError as exc:
            raise ValueError(f"Priority must be one of: {_allowed_values(Priority)}") from exc
    raise ValueError(f"Priority must be one of: {_allowed_values(Priority)}")


def _coerce_status(value: Status | str) -> Status:
    if isinstance(value, Status):
        return value
    if isinstance(value, str):
        try:
            return Status(value)
        except ValueError as exc:
            raise ValueError(f"Status must be one of: {_allowed_values(Status)}") from exc
    raise ValueError(f"Status must be one of: {_allowed_values(Status)}")


def _coerce_completed(value: bool) -> bool:
    if not isinstance(value, bool):
        raise ValueError("Completed must be true or false")
    return value


def _normalize_category(value: str | None) -> str:
    stripped = (value or "").strip()
    return stripped or "Other"


def _validate_user_id(user_id: int) -> int:
    if not isinstance(user_id, int) or user_id <= 0:
        raise ValueError("Valid user ID is required")
    return user_id


class TaskService:
    def __init__(self, dao: TaskDAO | None = None):
        self.dao = dao or TaskDAO()

    def _normalize_title(self, title: str) -> str:
        normalized_title = title.strip()
        if len(normalized_title) < 3:
            raise ValueError("Title must be at least 3 characters long")
        return normalized_title

    def _normalize_description(self, description: str) -> str:
        return description.strip()

    def create_task(
        self,
        title: str,
        description: str,
        priority: Priority,
        due_date: date | None = None,
        category: str = "Other",
        *,
        user_id: int,
    ) -> Task:
        owner_id = _validate_user_id(user_id)
        normalized_priority = _coerce_priority(priority)

        task = Task(
            title=self._normalize_title(title),
            description=self._normalize_description(description),
            priority=normalized_priority,
            status=Status.pending,
            category=_normalize_category(category),
            due_date=due_date,
            completed=False,
            user_id=owner_id,
        )

        return self.dao.create(task)

    def get_all_tasks(self, user_id: int) -> list[Task]:
        return self.dao.get_all_for_user(_validate_user_id(user_id))

    def get_task_by_id(self, task_id: int, user_id: int) -> Task:
        task = self.dao.get_by_id_for_user(task_id, _validate_user_id(user_id))
        if not task:
            raise ValueError("Task not found")
        return task

    def mark_complete(self, task_id: int, user_id: int) -> Task:
        task = self.get_task_by_id(task_id, user_id)
        task.status = Status.done
        task.completed = True
        return self.dao.update(task)

    def mark_pending(self, task_id: int, user_id: int) -> Task:
        task = self.get_task_by_id(task_id, user_id)
        task.status = Status.pending
        task.completed = False
        return self.dao.update(task)

    def delete_task(self, task_id: int, user_id: int) -> None:
        owner_id = _validate_user_id(user_id)
        if not self.dao.delete_for_user(task_id, owner_id):
            raise ValueError("Task not found")

    def delete_all_tasks(self, user_id: int) -> int:
        return self.dao.delete_all_for_user(_validate_user_id(user_id))

    def update_task(self, task_id: int, user_id: int, **updates) -> Task:
        task = self.get_task_by_id(task_id, user_id)

        allowed_fields = {
            "title",
            "description",
            "priority",
            "status",
            "due_date",
            "completed",
            "category",
        }

        original_status = task.status
        original_completed = task.completed

        for key, value in updates.items():
            if key not in allowed_fields:
                raise ValueError(f"Invalid field: {key}")
            if key == "priority":
                value = _coerce_priority(value)
            elif key == "status":
                value = _coerce_status(value)
            elif key == "completed":
                value = _coerce_completed(value)
            setattr(task, key, value)

        if "title" in updates:
            task.title = self._normalize_title(task.title)
        if "description" in updates:
            task.description = self._normalize_description(task.description)
        if "category" in updates:
            task.category = _normalize_category(task.category)
        if "status" in updates:
            task.completed = task.status == Status.done
        elif "completed" in updates:
            if task.completed:
                task.status = Status.done
            elif original_completed and original_status == Status.done:
                task.status = Status.pending

        return self.dao.update(task)
