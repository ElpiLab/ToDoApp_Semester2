import pytest

from student_task_manager.ui.pages import completion_progress_summary, is_valid_email


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
