from datetime import date

import pytest

from student_task_manager.data_access.dao import TaskDAO
from student_task_manager.domain.models import Priority, Status
from student_task_manager.services.task_service import TaskService


@pytest.fixture
def service_with_database(seeded_test_engine) -> TaskService:
    return TaskService(dao=TaskDAO())


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


def test_integration_filter_tasks_uses_persisted_records(
    service_with_database: TaskService,
) -> None:
    high_task = service_with_database.create_task(
        title="High priority integration task",
        description="Should match priority filter",
        priority=Priority.high,
        user_id=1,
    )
    low_task = service_with_database.create_task(
        title="Low priority integration task",
        description="Should stay open",
        priority=Priority.low,
        user_id=1,
    )
    assert high_task.id is not None
    assert low_task.id is not None
    service_with_database.mark_complete(high_task.id, user_id=1)

    open_low_tasks = service_with_database.filter_tasks(
        user_id=1,
        status=Status.created,
        priority=Priority.low,
    )

    assert [task.title for task in open_low_tasks] == ["Low priority integration task"]


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
