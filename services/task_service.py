from domain.models import Task, Priority, Status
from data.dao import TaskDAO
from datetime import date


class TaskService:

    def __init__(self):
        self.dao = TaskDAO()

    # 🔹 CREATE TASK (User Story 1 + Validation)
    def create_task(self, title: str, description: str,
                    priority: Priority, due_date: date | None) -> Task:

        # ✅ Validation (from requirements)
        if len(title) < 3:
            raise ValueError("Title must be at least 3 characters long")

        if len(description) < 5:
            raise ValueError("Description must be at least 5 characters long")

        if priority not in Priority:
            raise ValueError("Invalid priority value")

        # Create task object
        task = Task(
            title=title,
            description=description,
            priority=priority,
            status=Status.created,
            due_date=due_date,
            completed=False
        )

        return self.dao.create(task)

    # 🔹 VIEW ALL TASKS (User Story 2)
    def get_all_tasks(self):
        return self.dao.get_all()

    # 🔹 MARK AS COMPLETE (User Story 3)
    def mark_complete(self, task_id: int):
        task = self.dao.get_by_id(task_id)
        if not task:
            raise ValueError("Task not found")

        task.completed = True
        task.status = Status.done
        return self.dao.update(task)

    # 🔹 DELETE TASK (User Story 4)
    def delete_task(self, task_id: int):
        self.dao.delete(task_id)

    # 🔹 EDIT TASK (User Story 5)
    def update_task(self, task_id: int, **updates):
        task = self.dao.get_by_id(task_id)
        if not task:
            raise ValueError("Task not found")

        for key, value in updates.items():
            setattr(task, key, value)

        return self.dao.update(task)

    # 🔹 FILTER TASKS (User Story 8)
    def filter_tasks(self, status: Status | None = None,
                     priority: Priority | None = None):

        tasks = self.dao.get_all()

        if status:
            tasks = [t for t in tasks if t.status == status]

        if priority:
            tasks = [t for t in tasks if t.priority == priority]

        return tasks