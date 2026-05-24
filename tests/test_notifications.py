import pytest

from student_task_manager.ui.notifications import NotificationMenu


def test_notification_key_rejects_unpersisted_task_id() -> None:
    with pytest.raises(ValueError, match="Notification tasks must be persisted"):
        NotificationMenu.notification_key(None, "due_today")


def test_notification_key_uses_task_id_without_fallback_collision() -> None:
    assert NotificationMenu.notification_key(12, "due_today") == "due_today:12"
