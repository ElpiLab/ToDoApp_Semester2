from collections.abc import Callable
from datetime import date, timedelta
from typing import Any

from nicegui import ui

from student_task_manager.domain.models import Task


class NotificationMenu:
    def __init__(
        self,
        *,
        badge: Any,
        container: Any,
        read_keys: set[str],
        get_tasks: Callable[[], list[Task]],
        open_task_dialog: Callable[[Task], None],
        persist_read_keys: Callable[[set[str]], None],
    ) -> None:
        self.badge = badge
        self.container = container
        self.read_keys = read_keys
        self.get_tasks = get_tasks
        self.open_task_dialog = open_task_dialog
        self.persist_read_keys = persist_read_keys

    @staticmethod
    def notification_key(task_id: int | None, notification_type: str) -> str:
        if task_id is None:
            raise ValueError("Notification tasks must be persisted")
        return f"{notification_type}:{task_id}"

    def _persist_read_notifications(self) -> None:
        self.persist_read_keys(self.read_keys)

    def _mark_notification_read(self, key: str) -> None:
        self.read_keys.add(key)
        self._persist_read_notifications()
        self.render()

    def _mark_all_notifications_read(self, keys: list[str]) -> None:
        self.read_keys.update(keys)
        self._persist_read_notifications()
        self.render()

    def _open_notification_task(self, task: Task, key: str) -> None:
        self._mark_notification_read(key)
        self.open_task_dialog(task)

    def render(self) -> None:
        self.container.clear()
        all_tasks = self.get_tasks()
        today = date.today()
        tomorrow = today + timedelta(days=1)

        open_tasks = [t for t in all_tasks if not t.completed]

        notifications = []
        for task in open_tasks:
            if task.due_date and task.due_date < today:
                days_late = (today - task.due_date).days
                if days_late == 1:
                    sub = f"{task.title} was due yesterday"
                    when = "1d ago"
                else:
                    sub = f"{task.title} is {days_late} days late"
                    when = f"{days_late}d ago"
                notifications.append(
                    (
                        self.notification_key(task.id, "overdue"),
                        task,
                        "Task overdue",
                        sub,
                        when,
                        "error_outline",
                        "bg-rose-100",
                        "text-rose-600",
                        True,
                        0,
                        days_late,
                    )
                )
            elif task.due_date == today:
                notifications.append(
                    (
                        self.notification_key(task.id, "due_today"),
                        task,
                        "Due today",
                        f"{task.title} is due today",
                        "today",
                        "schedule",
                        "bg-amber-100",
                        "text-amber-600",
                        True,
                        1,
                        0,
                    )
                )
            elif task.due_date == tomorrow:
                notifications.append(
                    (
                        self.notification_key(task.id, "due_tomorrow"),
                        task,
                        "Due tomorrow",
                        f"{task.title} is due tomorrow",
                        "tomorrow",
                        "event",
                        "bg-amber-100",
                        "text-amber-600",
                        False,
                        2,
                        0,
                    )
                )
            elif task.priority.value == "high" and task.due_date is None:
                notifications.append(
                    (
                        self.notification_key(task.id, "high_no_due_date"),
                        task,
                        "High-priority reminder",
                        f"{task.title} has no due date",
                        "-",
                        "bookmark",
                        "bg-blue-100",
                        "text-blue-600",
                        False,
                        3,
                        0,
                    )
                )

        notifications.sort(
            key=lambda item: (
                0 if item[0] not in self.read_keys else 1,
                item[9],
                -item[10],
                -(item[1].id or 0),
            )
        )

        total_count = len(notifications)
        unread_keys = [key for key, *_ in notifications if key not in self.read_keys]
        unread_count = len(unread_keys)

        if unread_count == 0:
            self.badge.set_visibility(False)
        else:
            self.badge.set_text("")
            self.badge.set_visibility(True)

        max_show = 8

        with self.container:
            with ui.row().classes(
                "w-full items-center justify-between px-3 pt-3 pb-2 border-b border-slate-100"
            ):
                with ui.row().classes("items-center gap-2"):
                    ui.label("Notifications").classes("text-base font-semibold text-slate-900")
                    if unread_count:
                        with ui.element("div").classes(
                            "rounded-full bg-rose-600 px-2 py-0.5 "
                            "min-w-[20px] flex items-center justify-center"
                        ):
                            ui.label(str(unread_count)).classes("text-xs font-semibold text-white")
                if unread_count:
                    mark_all_btn = ui.button("Mark all read").props(
                        "flat no-caps dense color=grey-7"
                    )
                    mark_all_btn.classes("text-xs px-2 py-1 rounded-md")
                    mark_all_btn.on(
                        "click",
                        lambda keys=list(unread_keys): self._mark_all_notifications_read(keys),
                    )

            if not notifications:
                with ui.column().classes("w-full items-center gap-2 py-8"):
                    ui.icon("notifications_off", size="1.75rem").classes("text-slate-300")
                    ui.label("You're all caught up").classes("text-sm font-medium text-slate-700")
                    ui.label("No overdue or upcoming tasks.").classes("text-xs text-slate-500")
                return

            visible = notifications[:max_show]
            for idx, (
                key,
                task,
                title,
                sub,
                when,
                icon,
                bg_class,
                text_class,
                _,
                _,
                _,
            ) in enumerate(visible):
                is_unread = key not in self.read_keys
                bg_row = "bg-rose-50/40" if is_unread else ""
                border_class = "border-b border-slate-100" if idx < len(visible) - 1 else ""
                row = ui.element("div").classes(
                    "w-full flex items-start gap-3 px-3 py-3 "
                    "cursor-pointer hover:bg-stone-50 transition-colors "
                    f"{bg_row} {border_class}"
                )
                with row:
                    with ui.element("div").classes(
                        f"w-8 h-8 rounded-full {bg_class} flex items-center justify-center shrink-0"
                    ):
                        ui.icon(icon, size="1rem").classes(text_class)
                    with ui.column().classes("flex-1 min-w-0 gap-0"):
                        ui.label(title).classes("text-sm font-semibold text-slate-900")
                        ui.label(sub).classes("text-xs text-slate-500 truncate")
                    with ui.column().classes("items-end gap-1 shrink-0"):
                        ui.label(when).classes("text-xs text-slate-500")
                        if is_unread:
                            ui.element("div").classes("w-2 h-2 rounded-full bg-emerald-600")
                row.on(
                    "click",
                    lambda selected_task=task, selected_key=key: self._open_notification_task(
                        selected_task, selected_key
                    ),
                )

            if total_count > max_show:
                ui.label(f"+ {total_count - max_show} more").classes(
                    "text-xs text-slate-400 px-3 pt-1"
                )
