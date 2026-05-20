import pytest

from student_task_manager.ui.pages import is_valid_email


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
