from datetime import date

from data_access.dao import TaskDAO
from domain.models import Priority, Status, Task


class TaskService:
    def __init__(self):
        self.dao = TaskDAO()

    def create_task(
        self,
        title: str,
        description: str,
        priority: Priority,
        due_date: date | None = None,
    ) -> Task:
        title = title.strip()
        description = description.strip()

        if len(title) < 3:
            raise ValueError("Title must be at least 3 characters long")

        if len(description) < 5:
            raise ValueError("Description must be at least 5 characters long")

        if priority is None:
            raise ValueError("Priority is required")

        task = Task(
            title=title,
            description=description,
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
        task.completed = True
        task.status = Status.done
        return self.dao.update(task)

    def delete_task(self, task_id: int) -> None:
        task = self.get_task_by_id(task_id)
        self.dao.delete(task.id)

    def update_task(self, task_id: int, **updates) -> Task:
        task = self.get_task_by_id(task_id)

        allowed_fields = {"title", "description", "priority", "status", "due_date", "completed"}

        for key, value in updates.items():
            if key not in allowed_fields:
                raise ValueError(f"Invalid field: {key}")
            setattr(task, key, value)

        if "title" in updates and len(task.title.strip()) < 3:
            raise ValueError("Title must be at least 3 characters long")

        if "description" in updates and len(task.description.strip()) < 5:
            raise ValueError("Description must be at least 5 characters long")

        if task.status == Status.done:
            task.completed = True

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