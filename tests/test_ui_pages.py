from datetime import date, timedelta

import pytest

from student_task_manager.ui.view_helpers import (
    TASK_CATEGORY_OPTIONS,
    calendar_sidebar_border_class,
    completion_progress_summary,
    is_valid_email,
    status_display_label,
    task_matches_status_filter,
)
from student_task_manager.domain.models import Status, Task


def test_task_category_options_include_other_default() -> None:
    assert TASK_CATEGORY_OPTIONS == [
        "Project",
        "Exam",
        "Assignment",
        "Research",
        "Reading",
        "Personal",
        "Other",
    ]


@pytest.mark.parametrize(
    ("completed_count", "total_count", "expected"),
    [
        (0, 0, ("0%", "No tasks yet")),
        (0, 3, ("0%", "0 of 3 tasks done")),
        (3, 6, ("50%", "3 of 6 tasks done")),
        (1, 1, ("100%", "1 of 1 task done")),
    ],
)
def test_completion_progress_summary(
    completed_count: int,
    total_count: int,
    expected: tuple[str, str],
) -> None:
    assert completion_progress_summary(completed_count, total_count) == expected


@pytest.mark.parametrize(
    ("completed_count", "total_count", "expected"),
    [
        (0, 0, ("0%", "Nothing due this week")),
        (0, 3, ("0%", "0 of 3 due this week")),
        (3, 6, ("50%", "3 of 6 due this week")),
        (1, 1, ("100%", "1 of 1 due this week")),
    ],
)
def test_completion_progress_summary_with_period_label(
    completed_count: int,
    total_count: int,
    expected: tuple[str, str],
) -> None:
    assert (
        completion_progress_summary(completed_count, total_count, period_label="due this week")
        == expected
    )


@pytest.mark.parametrize(
    ("status_value", "expected"),
    [
        ("created", "To do"),
        ("pending", "To do"),
        ("open", "To do"),
        ("in_progress", "In Progress"),
        ("done", "Done"),
        ("overdue", "Overdue"),
    ],
)
def test_status_display_label_uses_consistent_task_status_terms(
    status_value: str,
    expected: str,
) -> None:
    assert status_display_label(status_value) == expected


@pytest.mark.parametrize(
    ("status", "completed", "status_filter", "expected"),
    [
        (Status.pending, False, "to_do", True),
        (Status.created, False, "to_do", True),
        (Status.in_progress, False, "to_do", False),
        (Status.in_progress, False, "in_progress", True),
        (Status.done, True, "in_progress", False),
        (Status.done, True, "done", True),
        (Status.pending, True, "done", True),
        (Status.pending, False, "all", True),
    ],
)
def test_task_matches_status_filter_matches_visible_status_sections(
    status: Status,
    completed: bool,
    status_filter: str,
    expected: bool,
) -> None:
    task = Task(
        title="Example",
        description="",
        status=status,
        completed=completed,
        user_id=1,
    )

    assert task_matches_status_filter(task, status_filter) is expected


@pytest.mark.parametrize(
    "email",
    [
        "student@example.com",
        "first.last@school.example.ch",
    ],
)
def test_is_valid_email_accepts_basic_addresses(email: str) -> None:
    assert is_valid_email(email)


@pytest.mark.parametrize(
    "email",
    [
        "",
        ".@.",
        "student",
        "student@",
        "student@example",
        "student@.com",
        "student example@example.com",
    ],
)
def test_is_valid_email_rejects_incomplete_addresses(email: str) -> None:
    assert not is_valid_email(email)


@pytest.mark.parametrize(
    ("priority", "due_offset_days", "completed", "expected"),
    [
        ("high", -1, False, "border-rose-500"),
        ("high", 4, False, "border-rose-400"),
        ("medium", 4, False, "border-amber-400"),
        ("low", 4, False, "border-emerald-400"),
        ("high", -1, True, "border-slate-300"),
    ],
)
def test_calendar_sidebar_border_class_matches_task_state_and_priority(
    priority: str,
    due_offset_days: int,
    completed: bool,
    expected: str,
) -> None:
    today = date(2026, 5, 23)
    due_date = today + timedelta(days=due_offset_days)

    assert calendar_sidebar_border_class(priority, due_date, today, completed) == expected
