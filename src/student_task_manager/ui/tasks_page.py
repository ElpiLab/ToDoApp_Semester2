from collections.abc import Callable
from datetime import date

from nicegui import ui

from student_task_manager.domain.models import Task
from student_task_manager.ui.view_helpers import (
    category_display,
    category_pill_class,
    priority_pill_class,
    priority_rail_class,
    relative_due_text,
    status_display_label,
)


def render_empty_state() -> None:
    with ui.column().classes("w-full items-center gap-3 px-6 py-12 text-center"):
        ui.icon("inbox", size="3rem").classes("text-slate-300")
        ui.label("No matching tasks").classes("text-lg font-medium text-slate-700")
        ui.label("Create a new task or adjust your filters to see more results.").classes(
            "text-sm text-slate-500"
        )


def render_list(
    tasks: list[Task],
    *,
    on_complete: Callable[[int], None],
    on_reopen: Callable[[int], None],
    on_delete: Callable[[int], None],
    on_edit: Callable[[Task], None],
    on_status_change: Callable[[int, str], None],
) -> None:
    today = date.today()
    priority_short = {"high": "HIGH", "medium": "MED", "low": "LOW"}

    overdue: list[Task] = []
    open_bucket: list[Task] = []
    in_progress_bucket: list[Task] = []
    done_bucket: list[Task] = []

    for task in tasks:
        if task.completed:
            done_bucket.append(task)
        elif task.due_date is not None and task.due_date < today:
            overdue.append(task)
        elif task.status.value == "in_progress":
            in_progress_bucket.append(task)
        else:
            open_bucket.append(task)

    overdue.sort(key=lambda t: t.due_date or date.max)
    open_bucket.sort(key=lambda t: t.due_date or date.max)
    in_progress_bucket.sort(key=lambda t: t.due_date or date.max)
    done_bucket.sort(key=lambda t: t.due_date or date.max, reverse=True)

    def status_pill(bucket_key: str) -> tuple[str, str, str]:
        if bucket_key == "overdue":
            return status_display_label("overdue"), "bg-rose-500", "bg-rose-100 text-rose-700"
        if bucket_key == "in_progress":
            return (
                status_display_label("in_progress"),
                "bg-blue-500",
                "bg-blue-100 text-blue-700",
            )
        if bucket_key == "done":
            return (
                status_display_label("done"),
                "bg-emerald-500",
                "bg-emerald-100 text-emerald-800",
            )
        return status_display_label("open"), "bg-slate-500", "bg-slate-100 text-slate-700"

    def render_row(task: Task, bucket_key: str) -> None:
        assert task.id is not None
        is_done = bucket_key == "done"
        is_overdue = bucket_key == "overdue"

        row_bg = "bg-rose-50/60" if is_overdue else "bg-white"
        row = ui.row().classes(
            "w-full items-center gap-3 px-4 py-3.5 cursor-pointer transition-colors group "
            f"{row_bg} hover:bg-slate-50/80"
        )
        row.on("click", lambda current_task=task: on_edit(current_task))
        with row:
            if is_done:
                check_classes = (
                    "flex-none w-6 h-6 rounded-full flex items-center justify-center "
                    "bg-emerald-500 text-white cursor-pointer"
                )
            elif is_overdue:
                check_classes = (
                    "flex-none w-6 h-6 rounded-full border-2 border-rose-400 "
                    "bg-white hover:bg-rose-50 cursor-pointer"
                )
            else:
                check_classes = (
                    "flex-none w-6 h-6 rounded-full border-2 border-slate-300 "
                    "bg-white hover:border-slate-500 cursor-pointer"
                )
            check_btn = ui.element("div").classes(check_classes)
            check_btn.on(
                "click.stop",
                lambda task_id=task.id, done=is_done: (
                    on_reopen(task_id) if done else on_complete(task_id)
                ),
            )
            with check_btn:
                if is_done:
                    ui.icon("check").classes("text-sm")

            accent = "bg-rose-300" if task.priority.value == "high" else "bg-emerald-300"
            ui.element("div").classes(f"flex-none w-1 h-10 rounded-full {accent}")

            with ui.column().classes("flex-1 min-w-0 gap-0.5"):
                title_classes = "text-sm font-semibold truncate w-full"
                if is_done:
                    title_classes += " line-through text-slate-400"
                elif is_overdue:
                    title_classes += " text-rose-700"
                else:
                    title_classes += " text-slate-900"
                ui.label(task.title).classes(title_classes)

                description_text = (task.description or "").strip()
                if description_text:
                    ui.label(description_text).classes("text-xs text-slate-500 truncate w-full")

                meta_parts = [category_display(task.category)]
                if task.due_date:
                    meta_parts.append(f"Due {task.due_date.strftime('%b')} {task.due_date.day}")
                ui.label(" · ".join(meta_parts)).classes("text-xs text-slate-500")

            pill_label, dot_color, pill_bg = status_pill(bucket_key)
            with ui.row().classes("flex-none w-[184px] items-center justify-end gap-3"):
                ui.label(priority_short[task.priority.value]).classes(
                    "w-12 text-center text-xs font-bold tracking-wider rounded px-2 py-1 "
                    f"{priority_pill_class(task.priority.value)}"
                )

                status_pill_el = ui.element("div").classes(
                    "w-28 flex items-center justify-center gap-1.5 rounded-full px-2.5 py-1 "
                    f"cursor-pointer hover:opacity-80 transition-opacity {pill_bg}"
                )
                with status_pill_el:
                    ui.element("div").classes(f"w-1.5 h-1.5 rounded-full {dot_color}")
                    ui.label(pill_label).classes("text-xs font-medium")
                    status_menu = ui.menu().props('anchor="bottom right" self="top right"')
                    with status_menu, ui.column().classes("p-1 gap-0 min-w-[140px]"):
                        for opt_label, opt_status in (
                            (status_display_label("pending"), "pending"),
                            (status_display_label("in_progress"), "in_progress"),
                            (status_display_label("done"), "done"),
                        ):
                            opt_btn = ui.button(opt_label).props(
                                "flat no-caps align=left color=grey-8"
                            )
                            opt_btn.classes("w-full justify-start px-2 py-1 rounded-md")

                            def pick_status(
                                e=None,
                                tid=task.id,
                                s=opt_status,
                                m=status_menu,
                            ) -> None:
                                m.close()
                                on_status_change(tid, s)

                            opt_btn.on("click", pick_status)
                status_pill_el.on("click.stop", lambda m=status_menu: m.open())

            delete_btn = (
                ui.button(icon="delete_outline")
                .props("flat round dense color=grey-5")
                .classes("opacity-0 group-hover:opacity-100 transition-opacity")
            )
            delete_btn.tooltip("Delete task")
            delete_btn.on("click.stop", lambda task_id=task.id: on_delete(task_id))

    sections = [
        (status_display_label("overdue"), overdue, "bg-rose-500", "overdue"),
        (status_display_label("open"), open_bucket, "bg-slate-700", "open"),
        (status_display_label("in_progress"), in_progress_bucket, "bg-blue-500", "in_progress"),
        (status_display_label("done"), done_bucket, "bg-emerald-500", "done"),
    ]

    first_section = True
    for label, bucket, dot_class, key in sections:
        if not bucket:
            continue
        with ui.row().classes(
            "w-full items-center gap-3 px-1 pb-3 " + ("pt-1" if first_section else "pt-8")
        ):
            ui.element("div").classes(f"w-2.5 h-2.5 rounded-full {dot_class}")
            ui.label(label.upper()).classes(
                "text-xs font-bold uppercase tracking-widest text-slate-700"
            )
            ui.label(str(len(bucket))).classes("text-xs font-medium text-slate-400 ml-1")
            ui.element("div").classes("flex-1 h-px bg-slate-200 ml-2")
        first_section = False

        with ui.card().classes("w-full rounded-2xl shadow-sm border-0 p-0 overflow-hidden"):
            for idx, task in enumerate(bucket):
                if idx > 0:
                    ui.separator()
                render_row(task, key)


def render_board(
    tasks: list[Task],
    *,
    on_edit: Callable[[Task], None],
    on_add_task: Callable[[], None],
    on_drag_start: Callable[[int], None],
    on_drop_status: Callable[[str], None],
) -> None:
    todo_tasks = [t for t in tasks if t.status.value in ("created", "pending")]
    in_progress_tasks = [t for t in tasks if t.status.value == "in_progress"]
    done_tasks = [t for t in tasks if t.status.value == "done"]

    columns = [
        ("To do", todo_tasks, "bg-slate-400", "text-slate-700", "pending"),
        (
            status_display_label("in_progress"),
            in_progress_tasks,
            "bg-blue-500",
            "text-blue-700",
            "in_progress",
        ),
        (
            status_display_label("done"),
            done_tasks,
            "bg-emerald-500",
            "text-emerald-700",
            "done",
        ),
    ]

    today = date.today()
    highlight_classes = "!ring-2 !ring-emerald-500 !bg-stone-300"

    def enter_column(card, depth: dict[str, int]) -> None:
        depth["d"] += 1
        if depth["d"] == 1:
            card.classes(add=highlight_classes)

    def leave_column(card, depth: dict[str, int]) -> None:
        depth["d"] -= 1
        if depth["d"] <= 0:
            depth["d"] = 0
            card.classes(remove=highlight_classes)

    def drop_on_column(card, depth: dict[str, int], status: str) -> None:
        depth["d"] = 0
        card.classes(remove=highlight_classes)
        on_drop_status(status)

    with ui.row().classes("w-full items-start gap-4"):
        for column_title, column_tasks, dot_class, text_class, target_status in columns:
            column_card = ui.card().classes(
                "flex flex-col flex-1 min-w-[280px] rounded-2xl shadow-none p-4 gap-3 !bg-stone-200"
            )
            column_depth = {"d": 0}
            column_card.on("dragover.prevent", lambda: None)
            column_card.on(
                "dragenter",
                lambda e=None, c=column_card, d=column_depth: enter_column(c, d),
            )
            column_card.on(
                "dragleave",
                lambda e=None, c=column_card, d=column_depth: leave_column(c, d),
            )
            column_card.on(
                "drop.prevent",
                lambda e=None, c=column_card, d=column_depth, s=target_status: drop_on_column(
                    c, d, s
                ),
            )
            with column_card:
                with ui.row().classes("w-full items-center gap-2"):
                    ui.element("div").classes(f"w-2 h-2 rounded-full {dot_class}")
                    ui.label(column_title).classes(f"text-sm font-semibold {text_class}")
                    ui.element("div").classes("grow")
                    ui.label(str(len(column_tasks))).classes(
                        "text-xs font-semibold text-slate-500 bg-slate-100 rounded-full px-2 py-1"
                    )

                for task in column_tasks:
                    assert task.id is not None
                    is_done = task.completed
                    is_late = task.due_date is not None and not is_done and task.due_date < today

                    card = (
                        ui.element("div")
                        .classes(
                            "w-full bg-white rounded-xl shadow-sm p-3 flex flex-col gap-2 "
                            "cursor-pointer hover:shadow-md transition-shadow "
                            f"border-l-4 {priority_rail_class(task.priority.value)}"
                        )
                        .props("draggable=true")
                    )
                    card.on("click", lambda e=None, current_task=task: on_edit(current_task))
                    card.on("dragstart", lambda e=None, task_id=task.id: on_drag_start(task_id))
                    with card:
                        title_classes = "font-medium text-slate-900 truncate w-full"
                        if is_done:
                            title_classes += " line-through text-slate-400"
                        ui.label(task.title).classes(title_classes)

                        description_text = (task.description or "").strip()
                        if description_text:
                            desc_classes = "text-xs text-slate-500 line-clamp-2"
                            if is_done:
                                desc_classes += " text-slate-400"
                            ui.label(description_text).classes(desc_classes)

                        with ui.row().classes("items-center gap-2 flex-wrap"):
                            ui.label(category_display(task.category)).classes(
                                f"text-xs rounded px-2 py-1 {category_pill_class(task.category)}"
                            )
                            ui.label(task.priority.value.upper()).classes(
                                "text-xs rounded px-2 py-1 "
                                f"{priority_pill_class(task.priority.value)}"
                            )
                        if task.due_date:
                            due_text = relative_due_text(task.due_date, today, is_done)
                            due_classes = (
                                "text-xs text-red-600 font-medium"
                                if is_late
                                else "text-xs text-slate-500"
                            )
                            ui.label(due_text).classes(due_classes)

                if not column_tasks and column_title != "To do":
                    empty_messages = {
                        status_display_label("in_progress"): "Nothing in progress",
                        "Done": "No completed tasks yet",
                    }
                    with ui.column().classes("w-full items-center justify-center py-8 gap-2"):
                        ui.icon("inbox", size="1.5rem").classes("text-slate-400")
                        ui.label(empty_messages.get(column_title, "No tasks")).classes(
                            "text-xs text-slate-500"
                        )

                if column_title == "To do":
                    add_btn = ui.element("div").classes(
                        "w-full rounded-xl border border-dashed border-slate-300 "
                        "hover:border-slate-400 hover:bg-slate-50 p-3 cursor-pointer "
                        "transition-colors"
                    )
                    with add_btn:
                        with ui.row().classes("items-center justify-center gap-1 text-slate-500"):
                            ui.icon("add").classes("text-base")
                            ui.label("Add task").classes("text-sm")
                    add_btn.on("click", lambda: on_add_task())
