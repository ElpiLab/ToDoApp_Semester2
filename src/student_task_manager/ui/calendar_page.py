import calendar as cal_module
from collections.abc import Callable
from datetime import date, timedelta
from typing import Any

from nicegui import ui

from student_task_manager.domain.models import Task
from student_task_manager.ui.view_helpers import (
    PRIORITY_RANK,
    calendar_sidebar_border_class,
)


def render_calendar_page(
    calendar_panel: Any,
    get_tasks: Callable[[], list[Task]],
    view_month: date,
    selected_date: date,
    calendar_filter_date: date | None,
    on_navigate_to_today: Callable[[], None],
    on_navigate_month: Callable[[int], None],
    on_select_date: Callable[[date], None],
    on_clear_calendar_filter: Callable[[], None],
    on_open_task_dialog: Callable[..., None],
) -> None:
    calendar_panel.clear()
    with calendar_panel:
        today = date.today()
        all_tasks = get_tasks()

        tasks_by_date: dict[date, list[Task]] = {}
        for task in all_tasks:
            if task.due_date:
                tasks_by_date.setdefault(task.due_date, []).append(task)

        month_start = view_month
        if view_month.month == 12:
            month_end = view_month.replace(year=view_month.year + 1, month=1) - timedelta(days=1)
        else:
            month_end = view_month.replace(month=view_month.month + 1) - timedelta(days=1)
        month_open_count = sum(
            1
            for task in all_tasks
            if task.due_date and not task.completed and month_start <= task.due_date <= month_end
        )

        upcoming_tasks = sorted(
            [task for task in all_tasks if task.due_date and not task.completed],
            key=lambda task: task.due_date or date.max,
        )

        with ui.row().classes("w-full items-center justify-between gap-4"):
            with ui.column().classes("gap-1"):
                ui.label(view_month.strftime("%B %Y")).classes(
                    "text-2xl font-semibold text-emerald-900"
                )
                plural = "s" if month_open_count != 1 else ""
                ui.label(f"{month_open_count} task{plural} due this month").classes(
                    "text-sm text-slate-500"
                )
            with ui.row().classes("items-center gap-1"):
                today_btn = ui.button("Today").props("flat dense no-caps color=green-9")
                today_btn.on("click", on_navigate_to_today)
                prev_btn = ui.button(icon="chevron_left").props("flat round dense color=grey-7")
                prev_btn.on("click", lambda: on_navigate_month(-1))
                next_btn = ui.button(icon="chevron_right").props("flat round dense color=grey-7")
                next_btn.on("click", lambda: on_navigate_month(1))

        with ui.row().classes("w-full items-stretch gap-4 flex-nowrap"):
            with ui.card().classes("flex-1 min-w-0 rounded-2xl !p-5 gap-3 !bg-white shadow-none"):
                with ui.element("div").classes("w-full grid grid-cols-7 gap-1 mb-1"):
                    for day_label in ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]:
                        ui.label(day_label).classes("text-xs text-slate-400 text-center")

                calendar = cal_module.Calendar(firstweekday=0)
                month_dates = list(calendar.itermonthdates(view_month.year, view_month.month))

                with ui.element("div").classes("w-full grid grid-cols-7 gap-1"):
                    for current_date in month_dates:
                        is_current_month = current_date.month == view_month.month
                        is_today_cell = current_date == today
                        is_selected = current_date == selected_date

                        if not is_current_month:
                            ui.element("div").classes("h-20")
                            continue

                        cell_tasks_all = tasks_by_date.get(current_date, [])
                        cell_tasks_open = [task for task in cell_tasks_all if not task.completed]
                        has_tasks = bool(cell_tasks_open)
                        is_overdue_day = has_tasks and current_date < today

                        cell_classes = (
                            "h-20 rounded-xl flex flex-col "
                            "items-center justify-center cursor-pointer "
                            "transition-colors relative"
                        )
                        if is_selected:
                            cell_classes += " ring-2 ring-emerald-300 bg-emerald-50"
                        elif is_today_cell:
                            cell_classes += " bg-emerald-100"
                        else:
                            cell_classes += " bg-stone-50 hover:bg-stone-100"

                        cell = ui.element("div").classes(cell_classes)
                        cell.on("click", lambda day=current_date: on_select_date(day))
                        with cell:
                            num_classes = "text-sm "
                            if is_today_cell or is_selected:
                                num_classes += "font-semibold text-emerald-900"
                            else:
                                num_classes += "text-slate-700"
                            ui.label(str(current_date.day)).classes(num_classes)
                            if has_tasks:
                                if is_overdue_day:
                                    dot_colors = ["bg-rose-500"]
                                else:
                                    priorities_present = {
                                        task.priority.value for task in cell_tasks_open
                                    }
                                    priority_dot_order = [
                                        ("high", "bg-rose-500"),
                                        ("medium", "bg-amber-500"),
                                        ("low", "bg-emerald-500"),
                                    ]
                                    dot_colors = [
                                        color
                                        for priority, color in priority_dot_order
                                        if priority in priorities_present
                                    ]
                                with ui.element("div").classes("absolute bottom-1 flex gap-0.5"):
                                    for color in dot_colors:
                                        ui.element("div").classes(f"w-1 h-1 rounded-full {color}")

            with ui.card().classes("w-80 shrink-0 rounded-2xl !p-5 gap-3 !bg-white shadow-none"):
                if calendar_filter_date:
                    panel_tasks = sorted(
                        tasks_by_date.get(calendar_filter_date, []),
                        key=lambda task: (
                            task.completed,
                            PRIORITY_RANK.get(task.priority.value, 99),
                            task.title.lower(),
                        ),
                    )
                    header_label = calendar_filter_date.strftime("%a %d %b").upper()
                else:
                    panel_tasks = upcoming_tasks
                    header_label = "UPCOMING TASKS"

                with ui.row().classes("w-full items-center justify-between"):
                    ui.label(header_label).classes(
                        "text-xs uppercase tracking-widest text-slate-500"
                    )
                    if calendar_filter_date:
                        clear_label = (
                            "Back to upcoming tasks" if panel_tasks else "Show upcoming tasks"
                        )
                        clear_btn = ui.button(clear_label).props("flat dense no-caps color=green-9")
                        clear_btn.on("click", on_clear_calendar_filter)

                if not panel_tasks:
                    with ui.column().classes("w-full items-center gap-2 py-6"):
                        ui.icon("event_available", size="2rem").classes("text-slate-300")
                        empty_text = (
                            "No tasks this day" if calendar_filter_date else "Nothing upcoming"
                        )
                        ui.label(empty_text).classes("text-sm text-slate-500")
                else:
                    for task in panel_tasks[:8]:
                        due_date = task.due_date
                        if due_date is None:
                            continue
                        is_late = not task.completed and due_date < today
                        days_diff = (due_date - today).days
                        if is_late:
                            hint_color = "text-rose-600"
                            hint_text = f"{due_date.strftime('%d %b')} \u00b7 {-days_diff}d overdue"
                        elif task.completed:
                            hint_color = "text-slate-400"
                            hint_text = f"{due_date.strftime('%d %b')} \u00b7 done"
                        else:
                            hint_color = "text-slate-500"
                            if days_diff == 0:
                                hint_text = f"{due_date.strftime('%d %b')} \u00b7 today"
                            else:
                                hint_text = f"{due_date.strftime('%d %b')} \u00b7 in {days_diff}d"
                        border_color = calendar_sidebar_border_class(
                            task.priority.value,
                            due_date,
                            today,
                            task.completed,
                        )
                        item = ui.element("div").classes(
                            "w-full pl-3 py-1 cursor-pointer "
                            f"border-l-4 {border_color} "
                            "hover:bg-stone-50 transition-colors"
                        )
                        with item:
                            title_classes = "text-sm font-semibold text-slate-900 truncate"
                            if task.completed:
                                title_classes += " line-through opacity-60"
                            ui.label(task.title).classes(title_classes)
                            ui.label(hint_text).classes(f"text-xs {hint_color}")
                        item.on(
                            "click",
                            lambda selected_task=task: on_open_task_dialog(selected_task),
                        )

                    if len(panel_tasks) > 8:
                        ui.label(f"+ {len(panel_tasks) - 8} more").classes(
                            "text-xs text-slate-400 pt-2"
                        )

                if calendar_filter_date:
                    add_label = f"+ Add task to {calendar_filter_date.strftime('%d %b')}"
                    add_btn = ui.element("div").classes(
                        "w-full rounded-xl border border-dashed "
                        "border-slate-300 hover:border-slate-400 "
                        "hover:bg-stone-50 p-3 cursor-pointer "
                        "transition-colors mt-2 text-center"
                    )
                    with add_btn:
                        ui.label(add_label).classes("text-sm text-slate-500")
                    add_btn.on(
                        "click",
                        lambda: on_open_task_dialog(default_due_date=calendar_filter_date),
                    )
