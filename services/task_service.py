from datetime import date

from data_access.dao import TaskDAO
from domain.models import Priority, Status, Task


class TaskService:
    def __init__(self, dao: TaskDAO | None = None):
        self.dao = dao or TaskDAO()

    def _normalize_title(self, title: str) -> str:
        normalized_title = title.strip()
        if len(normalized_title) < 3:
            raise ValueError("Title must be at least 3 characters long")
        return normalized_title

    def _normalize_description(self, description: str) -> str:
        normalized_description = description.strip()
        if len(normalized_description) < 5:
            raise ValueError("Description must be at least 5 characters long")
        return normalized_description

    def create_task(
        self,
        title: str,
        description: str,
        priority: Priority,
        due_date: date | None = None,
    ) -> Task:
        if priority is None:
            raise ValueError("Priority is required")

        task = Task(
            title=self._normalize_title(title),
            description=self._normalize_description(description),
            priority=priority,
            status=Status.created,
            due_date=due_date,
            completed=False,
        )

        return self.dao.create(task)

    def get_all_tasks(self) -> list[Task]:
        return self.dao.get_all()

    def get_task_by_id(self, task_id: int) -> Task:
        task = self.dao.get_by_id(task_id)
        if not task:
            raise ValueError("Task not found")
        return task

    def mark_complete(self, task_id: int) -> Task:
        task = self.get_task_by_id(task_id)
        task.status = Status.done
        task.completed = True
        return self.dao.update(task)

    def mark_pending(self, task_id: int) -> Task:
        task = self.get_task_by_id(task_id)
        task.status = Status.pending
        task.completed = False
        return self.dao.update(task)

    def delete_task(self, task_id: int) -> None:
        task = self.get_task_by_id(task_id)
        assert task.id is not None
        self.dao.delete(task.id)

    def update_task(self, task_id: int, **updates) -> Task:
        task = self.get_task_by_id(task_id)

        allowed_fields = {"title", "description", "priority", "status", "due_date", "completed"}

        for key, value in updates.items():
            if key not in allowed_fields:
                raise ValueError(f"Invalid field: {key}")
            setattr(task, key, value)

        task.title = self._normalize_title(task.title)
        task.description = self._normalize_description(task.description)
        if "status" in updates:
            task.completed = task.status == Status.done
        elif "completed" in updates:
            task.status = Status.done if task.completed else Status.pending

        return self.dao.update(task)

    def filter_tasks(
        self,
        status: Status | None = None,
        priority: Priority | None = None,
    ) -> list[Task]:
        tasks = self.dao.get_all()

        if status is not None:
            tasks = [task for task in tasks if task.status == status]

        if priority is not None:
            tasks = [task for task in tasks if task.priority == priority]

        return tasks
