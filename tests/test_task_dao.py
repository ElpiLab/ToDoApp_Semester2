from collections.abc import Iterator
from datetime import date

import pytest
from sqlalchemy.pool import StaticPool
from sqlmodel import Session, SQLModel, create_engine

from student_task_manager.data_access import dao as dao_module
from student_task_manager.data_access.dao import TaskDAO
from student_task_manager.domain.models import Priority, Status, Student, Task


@pytest.fixture
def task_dao(monkeypatch: pytest.MonkeyPatch) -> Iterator[TaskDAO]:
    test_engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(test_engine)
    with Session(test_engine) as session:
        session.add(
            Student(
                id=1,
                email="student@example.com",
                password_hash="not-used",
                full_name="Test Student",
            )
        )
        session.commit()

    monkeypatch.setattr(dao_module, "engine", test_engine)
    yield TaskDAO()


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
    stored_task = task_dao.get_by_id(task.id)
    assert stored_task is not None
    assert stored_task.title == "Persist database task"
    assert stored_task.priority == Priority.high


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

    stored_task = task_dao.get_by_id(task.id)
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

    task_dao.delete(task.id)

    assert task_dao.get_by_id(task.id) is None
