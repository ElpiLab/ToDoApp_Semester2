from collections.abc import Callable
from datetime import date, timedelta
from typing import Any

from nicegui import ui

from student_task_manager.domain.models import Task
from student_task_manager.ui.view_helpers import category_display, status_display_label


def render_analytics_page(
    analytics_panel: Any,
    get_tasks: Callable[[], list[Task]],
) -> None:
    analytics_panel.clear()
    with analytics_panel:
        all_tasks = get_tasks()
        today = date.today()
        total = len(all_tasks)

        open_tasks = [t for t in all_tasks if not t.completed]
        completed_tasks = [t for t in all_tasks if t.completed]
        overdue = [t for t in open_tasks if t.due_date and t.due_date < today]

        completion_pct = round(len(completed_tasks) / total * 100) if total else 0

        category_counts: dict[str, int] = {}
        category_done_counts: dict[str, int] = {}
        for t in all_tasks:
            key = category_display(t.category)
            category_counts[key] = category_counts.get(key, 0) + 1
            if t.completed:
                category_done_counts[key] = category_done_counts.get(key, 0) + 1
        category_items = sorted(category_counts.items(), key=lambda x: -x[1])

        done_count = len(completed_tasks)
        overdue_count = len(overdue)
        in_progress_count = sum(
            1
            for t in open_tasks
            if t.status.value == "in_progress" and not (t.due_date and t.due_date < today)
        )
        open_count = len(open_tasks) - in_progress_count - overdue_count

        priority_breakdown = []
        for p_value, p_label, p_color in [
            ("high", "HIGH", "#E11D48"),
            ("medium", "MEDIUM", "#F59E0B"),
            ("low", "LOW", "#10B981"),
        ]:
            p_tasks = [t for t in all_tasks if t.priority.value == p_value]
            p_done = sum(1 for t in p_tasks if t.completed)
            p_total = len(p_tasks)
            p_pct = round(p_done / p_total * 100) if p_total else 0
            priority_breakdown.append((p_label, p_done, p_total, p_pct, p_color))

        with ui.column().classes("gap-1"):
            ui.label("Analytics").classes("text-2xl font-semibold text-slate-900")
            ui.label("Your productivity at a glance").classes("text-sm text-slate-500")

        kpi_cards = [
            (
                "Total tasks",
                str(total),
                "text-slate-900",
            ),
            (
                "Completion",
                f"{completion_pct}%",
                "text-emerald-700",
            ),
            (
                "Done",
                str(len(completed_tasks)),
                "text-emerald-600",
            ),
            (
                "Overdue",
                str(len(overdue)),
                "text-rose-600",
            ),
        ]
        with ui.row().classes("w-full gap-3 flex-nowrap items-stretch"):
            for label, value, accent in kpi_cards:
                with ui.card().classes("w-44 rounded-xl shadow-sm !p-5 gap-2 justify-between"):
                    ui.label(label).classes("text-xs uppercase tracking-widest text-slate-500")
                    ui.label(value).classes(f"text-3xl font-semibold {accent} leading-none")

        with ui.row().classes("w-full items-stretch gap-4 flex-nowrap"):
            with ui.card().classes("flex-1 min-w-0 rounded-2xl shadow-sm !p-5 gap-3"):
                ui.label("Tasks by category").classes("text-lg font-semibold text-slate-900")
                ui.label("Total vs completed tasks in each category").classes(
                    "text-sm text-slate-400"
                )

                if not category_items:
                    with ui.column().classes("w-full items-center gap-2 py-10"):
                        ui.icon("inbox", size="2rem").classes("text-slate-300")
                        ui.label("No tasks yet").classes("text-sm text-slate-500")
                else:
                    ui.echart(
                        {
                            "tooltip": {"trigger": "axis"},
                            "grid": {
                                "left": 28,
                                "right": 12,
                                "top": 16,
                                "bottom": 28,
                                "containLabel": False,
                            },
                            "xAxis": {
                                "type": "category",
                                "data": [k for k, _ in category_items],
                                "axisLine": {"lineStyle": {"color": "#cbd5e1"}},
                                "axisLabel": {"color": "#475569"},
                            },
                            "yAxis": {
                                "type": "value",
                                "minInterval": 1,
                                "axisLine": {"show": False},
                                "axisTick": {"show": False},
                                "splitLine": {"lineStyle": {"color": "#e2e8f0"}},
                                "axisLabel": {"color": "#94a3b8"},
                            },
                            "series": [
                                {
                                    "name": "Total",
                                    "type": "bar",
                                    "data": [v for _, v in category_items],
                                    "barMaxWidth": 18,
                                    "itemStyle": {
                                        "color": "#A7F3D0",
                                        "borderRadius": [
                                            4,
                                            4,
                                            0,
                                            0,
                                        ],
                                    },
                                },
                                {
                                    "name": "Done",
                                    "type": "bar",
                                    "data": [
                                        category_done_counts.get(k, 0) for k, _ in category_items
                                    ],
                                    "barMaxWidth": 18,
                                    "itemStyle": {
                                        "color": "#10B981",
                                        "borderRadius": [
                                            4,
                                            4,
                                            0,
                                            0,
                                        ],
                                    },
                                },
                            ],
                        }
                    ).classes("w-full h-64")

                    with ui.row().classes(
                        "w-full items-center justify-center gap-5 mt-auto pt-3 flex-wrap"
                    ):
                        for legend_label, legend_color in [
                            ("Total", "bg-emerald-200"),
                            ("Done", "bg-emerald-500"),
                        ]:
                            with ui.row().classes("items-center gap-2"):
                                ui.element("div").classes(
                                    f"w-2.5 h-2.5 rounded-full {legend_color}"
                                )
                                ui.label(legend_label).classes("text-sm font-medium text-slate-700")

            with ui.card().classes("flex-1 min-w-0 rounded-2xl shadow-sm !p-5 gap-1"):
                ui.label("Status breakdown").classes("text-lg font-semibold text-slate-900")
                ui.label("Where your tasks stand right now").classes("text-sm text-slate-400")

                if total == 0:
                    with ui.column().classes("w-full items-center gap-2 py-10"):
                        ui.icon("celebration", size="2rem").classes("text-emerald-400")
                        ui.label("No tasks yet").classes("text-sm text-slate-500")
                else:
                    chart_wrapper = ui.element("div").classes(
                        "relative w-full flex items-center justify-center mt-2"
                    )
                    with chart_wrapper:
                        ui.echart(
                            {
                                "tooltip": {"trigger": "item"},
                                "series": [
                                    {
                                        "name": "Status",
                                        "type": "pie",
                                        "radius": ["62%", "85%"],
                                        "avoidLabelOverlap": False,
                                        "startAngle": 90,
                                        "itemStyle": {
                                            "borderColor": "#ffffff",
                                            "borderWidth": 4,
                                        },
                                        "label": {"show": False},
                                        "emphasis": {"scale": False},
                                        "data": [
                                            {
                                                "value": done_count,
                                                "name": status_display_label("done"),
                                                "itemStyle": {"color": "#10B981"},
                                            },
                                            {
                                                "value": in_progress_count,
                                                "name": status_display_label("in_progress"),
                                                "itemStyle": {"color": "#3B82F6"},
                                            },
                                            {
                                                "value": open_count,
                                                "name": status_display_label("open"),
                                                "itemStyle": {"color": "#CBD5E1"},
                                            },
                                            {
                                                "value": overdue_count,
                                                "name": "Overdue",
                                                "itemStyle": {"color": "#E11D48"},
                                            },
                                        ],
                                    }
                                ],
                            }
                        ).classes("w-64 h-64")

                        with ui.element("div").classes(
                            "absolute inset-0 flex flex-col "
                            "items-center justify-center pointer-events-none"
                        ):
                            ui.label(str(total)).classes("text-4xl font-semibold text-slate-900")
                            ui.label("TASKS").classes(
                                "text-xs font-semibold text-slate-500 tracking-widest mt-1"
                            )

                    with ui.row().classes(
                        "w-full items-center justify-center gap-4 mt-auto pt-3 flex-wrap"
                    ):
                        for label, count, color_class in [
                            (status_display_label("done"), done_count, "bg-emerald-500"),
                            (
                                status_display_label("in_progress"),
                                in_progress_count,
                                "bg-blue-500",
                            ),
                            (status_display_label("open"), open_count, "bg-slate-400"),
                            (status_display_label("overdue"), overdue_count, "bg-rose-600"),
                        ]:
                            with ui.row().classes("items-center gap-2"):
                                ui.element("div").classes(f"w-2.5 h-2.5 rounded-full {color_class}")
                                ui.label(f"{count} {label}").classes(
                                    "text-sm font-medium text-slate-700"
                                )

        with ui.row().classes("w-full items-stretch gap-4 flex-nowrap"):
            with ui.card().classes("flex-1 min-w-0 rounded-2xl shadow-sm !p-5 gap-3"):
                ui.label("Due-date heatmap").classes("text-lg font-semibold text-slate-900")
                ui.label("Workload over the next 12 weeks - darker means more tasks due").classes(
                    "text-sm text-slate-400"
                )

                weeks_count = 12
                heatmap_start = today - timedelta(days=today.weekday())
                horizon_end = heatmap_start + timedelta(weeks=weeks_count) - timedelta(days=1)

                due_counts: dict[date, int] = {}
                for t in open_tasks:
                    if t.due_date and heatmap_start <= t.due_date <= horizon_end:
                        due_counts[t.due_date] = due_counts.get(t.due_date, 0) + 1

                def color_for(count: int) -> str:
                    if count == 0:
                        return "bg-stone-200"
                    if count == 1:
                        return "bg-emerald-200"
                    if count == 2:
                        return "bg-emerald-400"
                    if count == 3:
                        return "bg-emerald-600"
                    return "bg-emerald-800"

                if not due_counts:
                    with ui.column().classes("w-full items-center gap-2 py-8"):
                        ui.icon("event_busy", size="2rem").classes("text-slate-300")
                        ui.label("No upcoming due dates").classes("text-sm text-slate-500")
                else:
                    with ui.row().classes("items-start gap-2 mt-3 w-full overflow-x-auto"):
                        with ui.column().classes("gap-1 pt-px shrink-0"):
                            for d_label in [
                                "Mon",
                                "Tue",
                                "Wed",
                                "Thu",
                                "Fri",
                                "Sat",
                                "Sun",
                            ]:
                                ui.label(d_label).classes("text-xs text-slate-400 h-5 leading-5")

                        with ui.element("div").classes(
                            "grid grid-flow-col grid-rows-7 gap-1 shrink-0"
                        ):
                            for w in range(weeks_count):
                                column_start = heatmap_start + timedelta(weeks=w)
                                for day_offset in range(7):
                                    d = column_start + timedelta(days=day_offset)
                                    count = due_counts.get(d, 0)
                                    cell = ui.element("div").classes(
                                        f"w-5 h-5 rounded {color_for(count)} cursor-default"
                                    )
                                    plural = "s" if count != 1 else ""
                                    cell.tooltip(
                                        f"{d.strftime('%a %b %d')}: {count} task{plural}"
                                        if count
                                        else d.strftime("%a %b %d")
                                    )

                    with ui.row().classes("w-full items-center gap-2 mt-3"):
                        ui.label("Less").classes("text-xs text-slate-400")
                        for level_class in [
                            "bg-stone-200",
                            "bg-emerald-200",
                            "bg-emerald-400",
                            "bg-emerald-600",
                            "bg-emerald-800",
                        ]:
                            ui.element("div").classes(f"w-3 h-3 rounded {level_class}")
                        ui.label("More").classes("text-xs text-slate-400")

            with ui.card().classes("flex-1 min-w-0 rounded-2xl shadow-sm !p-5 gap-3"):
                ui.label("By priority").classes("text-lg font-semibold text-slate-900")
                ui.label("Completion rate at each priority level").classes("text-sm text-slate-400")

                if total == 0:
                    with ui.column().classes("w-full items-center gap-2 py-10"):
                        ui.icon("flag", size="2rem").classes("text-slate-300")
                        ui.label("No tasks yet").classes("text-sm text-slate-500")
                else:
                    for (
                        p_label,
                        p_done,
                        p_total,
                        p_pct,
                        p_color,
                    ) in priority_breakdown:
                        with ui.row().classes("w-full items-center justify-between gap-2"):
                            ui.label(p_label).classes("text-sm font-semibold text-slate-900")
                            if p_total:
                                ui.label(f"{p_done}/{p_total} done · {p_pct}%").classes(
                                    "text-xs text-slate-500"
                                )
                            else:
                                ui.label("No tasks").classes("text-xs text-slate-400")
                        track = ui.element("div").classes(
                            "w-full h-2 rounded-full bg-stone-200 overflow-hidden"
                        )
                        with track:
                            ui.element("div").classes("h-full rounded-full").style(
                                f"width: {p_pct}%; background-color: {p_color};"
                            )
