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

    def get_all_for_user(self, user_id: int) -> list[Task]:
        return [task for task in self.tasks.values() if task.user_id == user_id]

    def get_by_id_for_user(self, task_id: int, user_id: int) -> Task | None:
        task = self.tasks.get(task_id)
        if task is None or task.user_id != user_id:
            return None
        return task

    def update(self, task: Task) -> Task:
        assert task.id is not None
        self.tasks[task.id] = task
        return task

    def delete_for_user(self, task_id: int, user_id: int) -> bool:
        task = self.tasks.get(task_id)
        if task is None or task.user_id != user_id:
            return False
        self.tasks.pop(task_id)
        return True

    def delete_all_for_user(self, user_id: int) -> int:
        task_ids = [task_id for task_id, task in self.tasks.items() if task.user_id == user_id]
        for task_id in task_ids:
            self.tasks.pop(task_id)
        return len(task_ids)


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
    assert task.status == Status.pending
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


def test_update_task_rejects_invalid_priority_before_persistence(service: TaskService) -> None:
    task = service.create_task(
        title="Review enum validation",
        description="Keep invalid values out of storage",
        priority=Priority.medium,
        user_id=1,
    )
    assert task.id is not None

    with pytest.raises(ValueError, match="Priority must be one of"):
        service.update_task(task.id, user_id=1, priority="urgent")

    assert service.get_task_by_id(task.id, user_id=1).priority == Priority.medium


def test_update_task_rejects_invalid_status_before_persistence(service: TaskService) -> None:
    task = service.create_task(
        title="Review status validation",
        description="Keep invalid values out of storage",
        priority=Priority.medium,
        user_id=1,
    )
    assert task.id is not None

    with pytest.raises(ValueError, match="Status must be one of"):
        service.update_task(task.id, user_id=1, status="blocked")

    assert service.get_task_by_id(task.id, user_id=1).status == Status.pending


def test_update_task_rejects_non_boolean_completed(service: TaskService) -> None:
    task = service.create_task(
        title="Review completion validation",
        description="Keep invalid booleans out of storage",
        priority=Priority.medium,
        user_id=1,
    )
    assert task.id is not None

    with pytest.raises(ValueError, match="Completed must be true or false"):
        service.update_task(task.id, user_id=1, completed="yes")

    assert service.get_task_by_id(task.id, user_id=1).completed is False


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


def test_delete_all_tasks_removes_only_requested_users_tasks(service: TaskService) -> None:
    service.create_task(
        title="Own first task",
        description="Delete this task",
        priority=Priority.high,
        user_id=1,
    )
    service.create_task(
        title="Own second task",
        description="Delete this task too",
        priority=Priority.medium,
        user_id=1,
    )
    service.create_task(
        title="Other task",
        description="Keep this task",
        priority=Priority.low,
        user_id=2,
    )

    deleted_count = service.delete_all_tasks(user_id=1)

    assert deleted_count == 2
    assert service.get_all_tasks(user_id=1) == []
    assert [task.title for task in service.get_all_tasks(user_id=2)] == ["Other task"]


def test_status_only_update_does_not_renormalize_legacy_short_title(
    service: TaskService,
) -> None:
    legacy_task = Task(
        id=99,
        title="Hi",
        description="Legacy imported task",
        priority=Priority.medium,
        status=Status.pending,
        completed=False,
        user_id=1,
    )
    service.dao.tasks[99] = legacy_task

    updated_task = service.update_task(99, user_id=1, status=Status.in_progress)

    assert updated_task.title == "Hi"
    assert updated_task.status == Status.in_progress
    assert updated_task.completed is False


def test_completed_false_does_not_demote_in_progress_task(service: TaskService) -> None:
    task = service.create_task(
        title="Work in progress",
        description="Keep active status",
        priority=Priority.medium,
        user_id=1,
    )
    assert task.id is not None
    service.update_task(task.id, user_id=1, status=Status.in_progress)

    updated_task = service.update_task(task.id, user_id=1, completed=False)

    assert updated_task.status == Status.in_progress
    assert updated_task.completed is False
