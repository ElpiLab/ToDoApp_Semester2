from datetime import date

import pytest
from sqlmodel import Session

from student_task_manager.data_access.dao import TaskDAO
from student_task_manager.domain.models import Priority, Status, Task


@pytest.fixture
def task_dao(seeded_test_engine) -> TaskDAO:
    assert seeded_test_engine is not None
    return TaskDAO(lambda: Session(seeded_test_engine))


def test_db_create_persists_task_with_generated_id(task_dao: TaskDAO) -> None:
    task = task_dao.create(
        Task(
            title="Persist database task",
            description="Stored through DAO",
            priority=Priority.high,
            due_date=date(2026, 5, 21),
            user_id=1,
        )
    )

    assert task.id is not None
    stored_task = task_dao.get_by_id_for_user(task.id, 1)
    assert stored_task is not None
    assert stored_task.title == "Persist database task"
    assert stored_task.priority == Priority.high


def test_db_user_scoped_queries_hide_other_users_tasks(task_dao: TaskDAO) -> None:
    own_task = task_dao.create(
        Task(
            title="Own persisted task",
            description="Visible to owner",
            priority=Priority.high,
            user_id=1,
        )
    )
    other_task = task_dao.create(
        Task(
            title="Other persisted task",
            description="Hidden from owner",
            priority=Priority.low,
            user_id=2,
        )
    )
    assert own_task.id is not None
    assert other_task.id is not None

    own_tasks = task_dao.get_all_for_user(1)

    assert [task.title for task in own_tasks] == ["Own persisted task"]
    assert task_dao.get_by_id_for_user(other_task.id, 1) is None


def test_db_update_persists_status_and_completion(task_dao: TaskDAO) -> None:
    task = task_dao.create(
        Task(
            title="Update persisted task",
            description="Move task to done",
            priority=Priority.medium,
            user_id=1,
        )
    )
    assert task.id is not None

    task.status = Status.done
    task.completed = True
    task_dao.update(task)

    stored_task = task_dao.get_by_id_for_user(task.id, 1)
    assert stored_task is not None
    assert stored_task.status == Status.done
    assert stored_task.completed is True


def test_db_delete_removes_task(task_dao: TaskDAO) -> None:
    task = task_dao.create(
        Task(
            title="Delete persisted task",
            description="Remove through DAO",
            priority=Priority.low,
            user_id=1,
        )
    )
    assert task.id is not None

    deleted = task_dao.delete_for_user(task.id, 1)

    assert deleted is True
    assert task_dao.get_by_id_for_user(task.id, 1) is None


def test_db_delete_for_user_rejects_other_users_task(task_dao: TaskDAO) -> None:
    task = task_dao.create(
        Task(
            title="Protected task",
            description="Only owner can delete",
            priority=Priority.low,
            user_id=1,
        )
    )
    assert task.id is not None

    deleted = task_dao.delete_for_user(task.id, 2)

    assert deleted is False
    assert task_dao.get_by_id_for_user(task.id, 1) is not None


def test_db_delete_all_for_user_removes_only_owned_tasks(task_dao: TaskDAO) -> None:
    own_task = task_dao.create(
        Task(
            title="Owned task",
            description="Delete this",
            priority=Priority.medium,
            user_id=1,
        )
    )
    other_task = task_dao.create(
        Task(
            title="Other task",
            description="Keep this",
            priority=Priority.low,
            user_id=2,
        )
    )
    assert own_task.id is not None
    assert other_task.id is not None

    deleted_count = task_dao.delete_all_for_user(1)

    assert deleted_count == 1
    assert task_dao.get_by_id_for_user(own_task.id, 1) is None
    assert task_dao.get_by_id_for_user(other_task.id, 2) is not None
