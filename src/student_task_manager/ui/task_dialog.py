from collections.abc import Callable
from datetime import date
from typing import Any

from nicegui import ui

from student_task_manager.domain.models import Task
from student_task_manager.ui.controllers import create_task, delete_task, update_task
from student_task_manager.ui.view_helpers import (
    TASK_CATEGORY_OPTIONS,
    category_display,
    status_display_label,
)


def _status_value_for_task(task: Task) -> str:
    return task.status.value


def _status_options_for_task() -> dict[str, str]:
    return {
        "pending": status_display_label("pending"),
        "in_progress": status_display_label("in_progress"),
        "done": status_display_label("done"),
    }


def open_task_dialog(
    task: Task | None = None,
    default_due_date: date | None = None,
    *,
    current_page: Callable[[], str],
    refresh_tasks: Callable[[], None],
    render_calendar: Callable[[], None],
    render_dashboard: Callable[[], None],
    render_analytics: Callable[[], None],
) -> None:
    is_edit = task is not None
    button_label = "Save changes" if is_edit else "Save task"
    if is_edit:
        default_due_iso = ""
    elif default_due_date:
        default_due_iso = default_due_date.isoformat()
    else:
        default_due_iso = ""

    with (
        ui.dialog().props("persistent") as dialog,
        ui.card().classes("w-[460px] max-w-full rounded-2xl p-6 gap-2"),
    ):
        with ui.row().classes("w-full items-center justify-between"):
            ui.label("EDIT TASK" if is_edit else "NEW TASK").classes(
                "text-xs uppercase tracking-widest text-slate-400"
            )
            close_btn = ui.button(icon="close").props("flat round dense color=grey-7")
            close_btn.tooltip("Close")
            close_btn.on("click", dialog.close)
        title_input = (
            ui.input(
                placeholder="What needs to be done?",
                value=task.title if is_edit and task else "",
            )
            .props('borderless autofocus dense hide-bottom-space input-class="text-xl"')
            .classes("w-full")
        )

        with ui.row().classes("w-full items-center justify-between flex-wrap"):
            priority_input = (
                ui.select(
                    {"low": "Low", "medium": "Medium", "high": "High"},
                    value=task.priority.value if is_edit and task else None,
                    label="Priority",
                )
                .props('dense outlined options-dense placeholder="Select..."')
                .classes("w-32")
            )

            category_options = list(TASK_CATEGORY_OPTIONS)
            category_initial = category_display(task.category) if is_edit and task else None
            if category_initial and category_initial not in category_options:
                category_options.append(category_initial)
            category_input = (
                ui.select(
                    category_options,
                    value=category_initial,
                    label="Category",
                    with_input=True,
                    new_value_mode="add-unique",
                )
                .props('dense outlined options-dense placeholder="Pick or type..."')
                .classes("w-28")
            )

            due_date_input = (
                ui.input(
                    value=(
                        task.due_date.isoformat()
                        if is_edit and task and task.due_date
                        else default_due_iso
                    ),
                    label="Due date",
                )
                .props('dense outlined type=date prepend-icon="event" hide-bottom-space')
                .classes("w-32 due-date-input")
            )

            status_input: Any | None = None
            if is_edit and task:
                status_input = (
                    ui.select(
                        _status_options_for_task(),
                        value=_status_value_for_task(task),
                    )
                    .props("dense outlined options-dense")
                    .classes("w-36")
                )

        description_input = (
            ui.textarea(
                placeholder="Add notes, context, or links...",
                value=task.description if is_edit and task else "",
            )
            .props("outlined autogrow")
            .classes("w-full")
        )

        add_another_checkbox: Any | None = None

        def save() -> None:
            priority_value = priority_input.value or "medium"
            category_value = (category_input.value or "").strip() or "Other"
            if is_edit:
                assert task is not None
                assert task.id is not None
                assert status_input is not None
                saved_task = update_task(
                    task.id,
                    title_input.value or "",
                    description_input.value or "",
                    priority_value,
                    status_input.value,
                    due_date_input.value or None,
                    category=category_value,
                )
            else:
                saved_task = create_task(
                    title_input.value or "",
                    description_input.value or "",
                    priority_value,
                    due_date_input.value or None,
                    category=category_value,
                )

            if saved_task is None:
                return

            keep_open = (
                not is_edit and add_another_checkbox is not None and add_another_checkbox.value
            )

            if keep_open:
                title_input.value = ""
                description_input.value = ""
                priority_input.value = None
                category_input.value = None
                due_date_input.value = default_due_iso
            else:
                dialog.close()

            refresh_tasks()
            page = current_page()
            if page == "calendar":
                render_calendar()
            if page == "dashboard":
                render_dashboard()
            if page == "analytics":
                render_analytics()

        def confirm_delete() -> None:
            with (
                ui.dialog() as confirm_dialog,
                ui.card().classes("w-[400px] max-w-full rounded-2xl p-6 gap-3"),
            ):
                ui.label("Delete this task?").classes("text-lg font-semibold text-slate-900")
                ui.label("This action cannot be undone.").classes("text-sm text-slate-500")

                def do_delete() -> None:
                    assert task is not None
                    assert task.id is not None
                    confirm_dialog.close()
                    if delete_task(task.id):
                        refresh_tasks()
                        dialog.close()

                with ui.row().classes("w-full justify-end gap-2 pt-2"):
                    ui.button("Cancel", on_click=confirm_dialog.close).props(
                        "flat color=grey-7 no-caps"
                    )
                    ui.button("Delete", on_click=do_delete).props(
                        "color=negative unelevated no-caps"
                    )
            confirm_dialog.open()

        with ui.row().classes(
            "w-full items-center justify-between pt-3 mt-1 border-t border-slate-100"
        ):
            if is_edit:
                ui.button("Delete", icon="delete", on_click=confirm_delete).props(
                    "flat color=negative no-caps"
                )
            else:
                add_another_checkbox = ui.checkbox("Add another")
            with ui.row().classes("gap-2"):
                ui.button("Cancel", on_click=dialog.close).props("flat color=grey-7 no-caps")
                ui.button(button_label, on_click=save).props("color=green-9 unelevated no-caps")

    dialog.open()
