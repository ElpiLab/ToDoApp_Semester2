from collections.abc import Callable
from datetime import date, datetime, timedelta
from typing import Any

from nicegui import ui

from student_task_manager.domain.models import Task
from student_task_manager.ui.view_helpers import (
    PRIORITY_RANK,
    category_display,
    completion_progress_summary,
    status_display_label,
)


def render_dashboard_page(
    dashboard_panel: Any,
    get_tasks: Callable[[], list[Task]],
    display_name: str,
    on_complete_task: Callable[[int], bool],
    on_refresh_tasks: Callable[[], None],
    on_open_task: Callable[[Task], None],
    on_switch_page: Callable[[str], None],
) -> None:
    dashboard_panel.clear()
    with dashboard_panel:
        tasks = get_tasks()
        today = date.today()
        tomorrow = today + timedelta(days=1)
        week_end = today + timedelta(days=7)

        open_tasks = [t for t in tasks if not t.completed]
        completed_tasks = [t for t in tasks if t.completed]
        overdue = [t for t in open_tasks if t.due_date and t.due_date < today]
        due_today = [t for t in open_tasks if t.due_date == today]
        due_tomorrow = [t for t in open_tasks if t.due_date == tomorrow]
        due_rest_of_week = sorted(
            [
                t
                for t in open_tasks
                if t.due_date and today + timedelta(days=2) <= t.due_date <= week_end
            ],
            key=lambda t: t.due_date or date.max,
        )

        hour = datetime.now().hour
        if hour < 12:
            greeting_text = "Good morning"
        elif hour < 17:
            greeting_text = "Good afternoon"
        else:
            greeting_text = "Good evening"

        def dashboard_quick_complete(task_id: int) -> None:
            if on_complete_task(task_id):
                render_dashboard_page(
                    dashboard_panel,
                    get_tasks,
                    display_name,
                    on_complete_task,
                    on_refresh_tasks,
                    on_open_task,
                    on_switch_page,
                )
                on_refresh_tasks()

        week_count = len(due_today) + len(due_tomorrow) + len(due_rest_of_week)

        attention_count = len(overdue) + len(due_today)
        if attention_count == 0:
            attention_msg = "nothing urgent today"
        else:
            plural = "s" if attention_count != 1 else ""
            attention_msg = f"{attention_count} item{plural} needs attention"
        hero_date = today.strftime("%a %d %b")
        hero_attention = attention_msg

        category_progress: list[tuple[str, int]] = []
        cats_seen = set()
        for t in tasks:
            key = (t.category or "").strip()
            if not key or key.lower() in cats_seen:
                continue
            cats_seen.add(key.lower())
            cat_tasks = [x for x in tasks if (x.category or "").lower() == key.lower()]
            if not cat_tasks:
                continue
            pct = round(sum(1 for x in cat_tasks if x.completed) / len(cat_tasks) * 100)
            category_progress.append((category_display(key), pct))
        category_progress = sorted(category_progress, key=lambda x: -x[1])[:3]

        overall_pct = round(len(completed_tasks) / len(tasks) * 100) if tasks else 0

        upcoming_tasks = sorted(
            [t for t in open_tasks if t.due_date],
            key=lambda t: (
                t.due_date or date.max,
                PRIORITY_RANK.get(t.priority.value, 99),
                t.title.lower(),
            ),
        )

        with ui.element("div").classes("w-full grid grid-cols-3 gap-4"):
            with ui.card().classes(
                "col-span-2 rounded-2xl !p-6 gap-2 !bg-emerald-900 !text-white shadow-none"
            ):
                first_name = display_name.split("@")[0].split()[0] if display_name else "there"
                ui.label(f"{greeting_text}, {first_name}").classes(
                    "text-2xl font-semibold leading-tight !text-white"
                )
                with ui.column().classes("gap-0 mt-2"):
                    ui.label(hero_date).classes("text-sm text-emerald-200")
                    ui.label(hero_attention).classes("text-sm text-emerald-200")

            oldest_overdue_days = max(
                ((today - t.due_date).days for t in overdue if t.due_date),
                default=0,
            )
            if overdue:
                plural = "s" if oldest_overdue_days != 1 else ""
                overdue_sub = f"Oldest {oldest_overdue_days} day{plural} late"
            else:
                overdue_sub = "All caught up"
            if week_count:
                plural = "s" if week_count != 1 else ""
                open_sub = f"{week_count} due this week"
            else:
                open_sub = "Nothing this week"
            week_tasks = [t for t in tasks if t.due_date and today <= t.due_date <= week_end]
            week_completed_count = sum(1 for t in week_tasks if t.completed)
            progress_value, progress_sub = completion_progress_summary(
                week_completed_count, len(week_tasks), period_label="due this week"
            )

            with ui.card().classes("rounded-2xl !p-5 gap-1 !bg-white shadow-none"):
                ui.label(str(len(open_tasks))).classes(
                    "text-3xl font-semibold text-slate-900 leading-none"
                )
                ui.label("ACTIVE").classes("text-xs uppercase tracking-widest text-slate-500 mt-2")
                ui.label(open_sub).classes("text-xs text-slate-500")

            with ui.card().classes("rounded-2xl !p-5 gap-1 !bg-emerald-100 shadow-none"):
                ui.label(progress_value).classes(
                    "text-3xl font-semibold text-emerald-900 leading-none"
                )
                ui.label("PROGRESS").classes(
                    "text-xs uppercase tracking-widest text-emerald-800 mt-2"
                )
                ui.label(progress_sub).classes("text-xs text-emerald-800")

            with ui.card().classes("rounded-2xl !p-5 gap-1 !bg-orange-100 shadow-none"):
                ui.label(str(len(overdue))).classes(
                    "text-3xl font-semibold text-orange-900 leading-none"
                )
                ui.label("OVERDUE").classes(
                    "text-xs uppercase tracking-widest text-orange-800 mt-2"
                )
                ui.label(overdue_sub).classes("text-xs text-orange-800")

            with ui.card().classes(
                "row-span-2 rounded-2xl !p-6 gap-3 !bg-emerald-900 !text-white shadow-none"
            ):
                ui.label("BY CATEGORY").classes(
                    "text-xs uppercase tracking-widest text-emerald-200"
                )
                for cat_label, pct in category_progress:
                    with ui.row().classes("w-full items-center justify-between"):
                        ui.label(cat_label).classes("text-sm !text-white")
                        ui.label(f"{pct}%").classes("text-sm text-emerald-200")
                    track = ui.element("div").classes(
                        "w-full h-1 rounded-full bg-emerald-800 overflow-hidden"
                    )
                    with track:
                        ui.element("div").classes("h-full bg-emerald-300 rounded-full").style(
                            f"width: {pct}%;"
                        )
                with ui.row().classes("w-full items-center justify-between mt-2"):
                    ui.label("Overall").classes("text-sm font-semibold !text-white")
                    ui.label(f"{overall_pct}%").classes("text-sm font-semibold text-emerald-200")
                track = ui.element("div").classes(
                    "w-full h-1 rounded-full bg-emerald-800 overflow-hidden"
                )
                with track:
                    ui.element("div").classes("h-full bg-emerald-300 rounded-full").style(
                        f"width: {overall_pct}%;"
                    )

            with ui.card().classes("col-span-2 rounded-2xl !p-5 gap-2 !bg-white shadow-none"):
                ui.label("UPCOMING TASKS").classes(
                    "text-xs uppercase tracking-widest text-slate-500"
                )
                if not upcoming_tasks:
                    with ui.column().classes("w-full items-center gap-2 py-6"):
                        ui.icon("event_available", size="2rem").classes("text-slate-300")
                        ui.label("Nothing upcoming").classes("text-sm font-semibold text-slate-700")
                else:
                    visible = upcoming_tasks[:4]
                    for idx, t in enumerate(visible):
                        due_date = t.due_date
                        if due_date is None:
                            continue
                        is_overdue = due_date < today
                        is_in_progress = t.status.value == "in_progress"
                        if is_overdue:
                            circle_class = "border-rose-500"
                            title_color = "text-rose-600"
                            pill_label = status_display_label("overdue")
                            pill_class = "bg-rose-100 text-rose-700"
                        elif is_in_progress:
                            circle_class = "border-emerald-500"
                            title_color = "text-slate-900"
                            pill_label = status_display_label("in_progress")
                            pill_class = "bg-emerald-100 text-emerald-700"
                        else:
                            circle_class = "border-slate-300"
                            title_color = "text-slate-900"
                            pill_label = status_display_label("open")
                            pill_class = "bg-slate-100 text-slate-600"
                        is_last = idx == len(visible) - 1
                        border_class = "" if is_last else " border-b border-slate-100"
                        row = ui.row().classes(
                            "w-full items-center gap-3 py-3 px-1 -mx-1 rounded-md "
                            "cursor-pointer hover:bg-stone-50 transition-colors" + border_class
                        )
                        with row:
                            circle = ui.element("div").classes(
                                f"w-5 h-5 rounded-full border-2 "
                                f"{circle_class} shrink-0 cursor-pointer"
                            )
                            circle.on(
                                "click.stop",
                                lambda task_id=t.id: dashboard_quick_complete(task_id),
                            )
                            circle.tooltip("Mark complete")
                            with ui.column().classes("flex-1 min-w-0 gap-0"):
                                title_classes = f"text-sm font-semibold {title_color} truncate"
                                ui.label(t.title).classes(title_classes)
                                cat = category_display(t.category)
                                date_str = due_date.strftime("%d %b")
                                ui.label(f"{cat} · {date_str}").classes("text-xs text-slate-500")
                            ui.label(pill_label).classes(
                                f"text-xs font-semibold rounded px-2 py-1 shrink-0 {pill_class}"
                            )
                        row.on("click", lambda task=t: on_open_task(task))

                    more_count = max(len(upcoming_tasks) - 4, 0)
                    view_all_label = (
                        f"View all tasks · +{more_count} more" if more_count else "View all tasks"
                    )
                    ui.button(
                        view_all_label,
                        on_click=lambda: on_switch_page("tasks"),
                    ).props("flat no-caps dense color=green-9").classes("text-xs self-start pt-1")
