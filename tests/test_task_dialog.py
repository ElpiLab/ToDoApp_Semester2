from student_task_manager.domain.models import Status, Task
from student_task_manager.ui.task_dialog import _status_options_for_task, _status_value_for_task


def test_status_value_for_task_returns_persisted_status() -> None:
    task = Task(title="Pending task", status=Status.pending, user_id=1)

    assert _status_value_for_task(task) == "pending"


def test_status_options_are_flat_three_state_options() -> None:
    assert _status_options_for_task() == {
        "pending": "To do",
        "in_progress": "In Progress",
        "done": "Done",
    }
