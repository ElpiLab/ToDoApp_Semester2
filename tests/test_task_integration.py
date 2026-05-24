from datetime import date

import pytest
from sqlmodel import Session

from student_task_manager.data_access.dao import TaskDAO
from student_task_manager.domain.models import Priority, Status
from student_task_manager.services.task_service import TaskService


@pytest.fixture
def service_with_database(seeded_test_engine) -> TaskService:
    assert seeded_test_engine is not None
    return TaskService(dao=TaskDAO(lambda: Session(seeded_test_engine)))


def test_integration_create_task_round_trips_through_database(
    service_with_database: TaskService,
) -> None:
    created_task = service_with_database.create_task(
        title="  Finish integration notes  ",
        description="  Confirm service and DAO path  ",
        priority=Priority.high,
        due_date=date(2026, 5, 22),
        category=" Project ",
        user_id=1,
    )
    assert created_task.id is not None

    stored_task = service_with_database.get_task_by_id(created_task.id, user_id=1)
    assert stored_task.title == "Finish integration notes"
    assert stored_task.description == "Confirm service and DAO path"
    assert stored_task.category == "Project"
    assert stored_task.due_date == date(2026, 5, 22)


def test_integration_complete_task_updates_persisted_state(
    service_with_database: TaskService,
) -> None:
    created_task = service_with_database.create_task(
        title="Complete integration task",
        description="Verify completed state is stored",
        priority=Priority.medium,
        user_id=1,
    )
    assert created_task.id is not None

    service_with_database.mark_complete(created_task.id, user_id=1)
    stored_task = service_with_database.get_task_by_id(created_task.id, user_id=1)

    assert stored_task.status == Status.done
    assert stored_task.completed is True


def test_integration_other_user_cannot_update_task(
    service_with_database: TaskService,
) -> None:
    created_task = service_with_database.create_task(
        title="Owner-only task",
        description="Other users cannot update this task",
        priority=Priority.high,
        user_id=1,
    )
    assert created_task.id is not None

    with pytest.raises(ValueError, match="Task not found"):
        service_with_database.update_task(
            created_task.id,
            user_id=2,
            title="Unauthorized edit",
        )

    stored_task = service_with_database.get_task_by_id(created_task.id, user_id=1)
    assert stored_task.title == "Owner-only task"


def test_integration_invalid_priority_update_does_not_corrupt_row(
    service_with_database: TaskService,
) -> None:
    created_task = service_with_database.create_task(
        title="Protected enum task",
        description="Reject invalid priorities before persistence",
        priority=Priority.medium,
        due_date=date(2026, 6, 2),
        user_id=1,
    )
    assert created_task.id is not None

    with pytest.raises(ValueError, match="Priority must be one of"):
        service_with_database.update_task(
            created_task.id,
            user_id=1,
            priority="urgent",
        )

    stored_task = service_with_database.get_task_by_id(created_task.id, user_id=1)
    assert stored_task.priority == Priority.medium
