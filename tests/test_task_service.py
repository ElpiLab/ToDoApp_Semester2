from datetime import date

import pytest

from student_task_manager.data_access.dao import TaskDAO
from student_task_manager.domain.models import Priority, Status, Task
from student_task_manager.services.task_service import TaskService


class FakeTaskDAO(TaskDAO):
    def __init__(self) -> None:
        self.tasks: dict[int, Task] = {}
        self.next_id = 1

    def create(self, task: Task) -> Task:
        task.id = self.next_id
        self.tasks[self.next_id] = task
        self.next_id += 1
        return task

    def get_all(self) -> list[Task]:
        return list(self.tasks.values())

    def get_all_for_user(self, user_id: int) -> list[Task]:
        return [task for task in self.tasks.values() if task.user_id == user_id]

    def get_by_id(self, task_id: int) -> Task | None:
        return self.tasks.get(task_id)

    def get_by_id_for_user(self, task_id: int, user_id: int) -> Task | None:
        task = self.tasks.get(task_id)
        if task is None or task.user_id != user_id:
            return None
        return task

    def update(self, task: Task) -> Task:
        assert task.id is not None
        self.tasks[task.id] = task
        return task

    def delete(self, task_id: int) -> None:
        self.tasks.pop(task_id, None)


@pytest.fixture
def service() -> TaskService:
    return TaskService(dao=FakeTaskDAO())


def test_create_task_trims_fields_and_sets_defaults(service: TaskService) -> None:
    task = service.create_task(
        title="  Finish OOP assignment  ",
        description="  Write the final class diagram  ",
        priority=Priority.high,
        due_date=date(2026, 5, 10),
        user_id=7,
    )

    assert task.id == 1
    assert task.title == "Finish OOP assignment"
    assert task.description == "Write the final class diagram"
    assert task.priority == Priority.high
    assert task.status == Status.created
    assert task.completed is False
    assert task.user_id == 7


def test_update_task_marks_done_tasks_as_completed(service: TaskService) -> None:
    task = service.create_task(
        title="Finish report",
        description="Write the testing summary",
        priority=Priority.medium,
        user_id=1,
    )

    assert task.id is not None
    updated_task = service.update_task(task.id, user_id=1, status=Status.done)

    assert updated_task.status == Status.done
    assert updated_task.completed is True


def test_update_task_reopens_completed_tasks_when_status_changes(service: TaskService) -> None:
    task = service.create_task(
        title="Prepare slides",
        description="Build the project presentation",
        priority=Priority.low,
        user_id=1,
    )
    assert task.id is not None
    service.mark_complete(task.id, user_id=1)

    reopened_task = service.update_task(task.id, user_id=1, status=Status.pending)

    assert reopened_task.status == Status.pending
    assert reopened_task.completed is False


def test_create_task_accepts_empty_description(service: TaskService) -> None:
    task = service.create_task(
        title="Read chapter six",
        description="",
        priority=Priority.medium,
        user_id=1,
    )

    assert task.description == ""


def test_get_all_tasks_returns_only_requested_user_tasks(service: TaskService) -> None:
    service.create_task(
        title="Own task",
        description="Visible to owner",
        priority=Priority.high,
        user_id=1,
    )
    service.create_task(
        title="Other task",
        description="Hidden from owner",
        priority=Priority.low,
        user_id=2,
    )

    tasks = service.get_all_tasks(user_id=1)

    assert [task.title for task in tasks] == ["Own task"]


def test_update_task_rejects_other_users_task(service: TaskService) -> None:
    task = service.create_task(
        title="Private task",
        description="Only owner can update",
        priority=Priority.medium,
        user_id=1,
    )
    assert task.id is not None

    with pytest.raises(ValueError, match="Task not found"):
        service.update_task(task.id, user_id=2, title="Changed by another user")
