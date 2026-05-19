import calendar as cal_module
from datetime import date, datetime, timedelta

from nicegui import ui

from ui.controllers import (
    change_task_status,
    complete_task,
    create_task,
    delete_task,
    get_tasks,
    mark_task_pending,
    update_task,
)


def get_priority_color(priority: str) -> str:
    if priority == "high":
        return "negative"
    if priority == "medium":
        return "warning"
    return "positive"


def get_status_color(status: str) -> str:
    if status == "done":
        return "positive"
    if status == "in_progress":
        return "primary"
    if status in ("pending", "created"):
        return "warning"
    return "secondary"


def status_display_label(status_value: str) -> str:
    if status_value in ("created", "pending"):
        return "To do"
    return status_value.replace("_", " ").title()


CATEGORY_PILL_CLASSES = {
    "project": "bg-teal-100 text-teal-700",
    "exam": "bg-rose-100 text-rose-700",
    "assignment": "bg-blue-100 text-blue-700",
    "reading": "bg-emerald-100 text-emerald-700",
    "other": "bg-slate-100 text-slate-700",
}

PRIORITY_PILL_CLASSES = {
    "low": "bg-emerald-100 text-emerald-700",
    "medium": "bg-amber-100 text-amber-700",
    "high": "bg-rose-100 text-rose-700",
}

PRIORITY_RANK = {"high": 0, "medium": 1, "low": 2}


def category_pill_class(value: str) -> str:
    return CATEGORY_PILL_CLASSES.get(
        (value or "").lower(), "bg-slate-100 text-slate-700"
    )


def priority_pill_class(value: str) -> str:
    return PRIORITY_PILL_CLASSES.get(
        (value or "").lower(), "bg-slate-100 text-slate-700"
    )


def category_display(value: str) -> str:
    stripped = (value or "").strip()
    return stripped.title() if stripped else "Other"


def format_due_date(due_date: date | None) -> str:
    return due_date.isoformat() if due_date else "No due date"


def relative_due_text(due_date: date, today: date, is_done: bool) -> str:
    formatted = due_date.strftime("%d %b")
    if is_done:
        return f"Due {formatted}"
    delta = (due_date - today).days
    if delta == 0:
        return f"Due {formatted} · today"
    if delta > 0:
        plural = "s" if delta != 1 else ""
        return f"Due {formatted} · in {delta} day{plural}"
    days_late = -delta
    plural = "s" if days_late != 1 else ""
    return f"Due {formatted} · {days_late} day{plural} late"


def normalize_query(value: str | None) -> str:
    return (value or "").strip().lower()


@ui.page("/")
def index_page():
    ui.query("body").classes("bg-stone-100")
    ui.query(".q-layout").props('view="lHh LpR fFf"')
    ui.add_head_html(
        "<style>"
        ".new-task-btn .q-btn__content { gap: 0; }"
        ".new-task-btn .q-btn__content .q-icon { font-size: 18px; }"
        ".new-task-btn .q-btn__content .q-icon.on-left { margin-right: 2px; }"
        ".new-task-btn .q-btn__content .q-icon.on-right { margin-left: 2px; }"
        ".q-drawer--mini .sidebar-hide { display: none !important; }"
        ".q-drawer--mini .nav-item "
        "{ padding-left: 0 !important; padding-right: 0 !important; }"
        ".q-drawer--mini .nav-item .q-btn__content "
        "{ justify-content: center; }"
        ".q-drawer--mini .nav-item .q-btn__content > *:not(.q-icon) "
        "{ display: none; }"
        ".q-drawer--mini .nav-item .q-btn__content .q-icon.on-left "
        "{ margin-right: 0; }"
        "</style>"
    )

    state = {
        "status": "all",
        "priority": "all",
        "category": "all",
        "sort": "due_date",
        "search": "",
        "view": "board",
        "dragging": None,
        "page": "dashboard",
        "view_month": date.today().replace(day=1),
        "selected_date": date.today(),
        "calendar_filter_date": None,
    }

    drawer_state = {"open": True}
    drawer = ui.left_drawer(
        value=True, top_corner=False, bottom_corner=True
    ).classes("bg-white text-slate-900 border-r border-slate-200").props(
        "width=260"
    )

    def toggle_sidebar() -> None:
        drawer_state["open"] = not drawer_state["open"]
        drawer.set_value(drawer_state["open"])
        expand_btn.set_visibility(not drawer_state["open"])

    with drawer:
        with ui.column().classes("w-full h-full pt-4 px-4 pb-4 gap-0"):
            with ui.row().classes(
                "w-full items-center pl-3 mb-2"
            ):
                ui.label("WORKSPACE").classes(
                    "text-xs uppercase tracking-widest text-slate-400 "
                    "flex-1 sidebar-hide"
                )
                collapse_btn = ui.button(icon="chevron_left").props(
                    "flat round dense color=grey-7"
                )
                collapse_btn.tooltip("Collapse sidebar")
                collapse_btn.on("click", toggle_sidebar)
            workspace_nav_container = ui.column().classes("w-full gap-2")
            nav_buttons: dict = {}

            def render_workspace_nav() -> None:
                workspace_nav_container.clear()
                with workspace_nav_container:
                    workspace_items = [
                        ("Dashboard", "dashboard", "dashboard"),
                        ("Tasks", "task_alt", "tasks"),
                        ("Calendar", "calendar_month", "calendar"),
                        ("Analytics", "analytics", "analytics"),
                    ]
                    for label, icon, key in workspace_items:
                        is_active = state["page"] == key
                        item_classes = "w-full px-3 py-2 rounded-lg nav-item"
                        if is_active:
                            btn = (
                                ui.button(label, icon=icon)
                                .props("flat no-caps align=left color=teal-7")
                                .classes(
                                    f"{item_classes} bg-teal-50 font-semibold"
                                )
                            )
                        else:
                            btn = (
                                ui.button(label, icon=icon)
                                .props("flat no-caps align=left color=grey-8")
                                .classes(item_classes)
                            )
                        if key in ("dashboard", "tasks", "calendar", "analytics"):
                            btn.on(
                                "click", lambda k=key: switch_to_page(k)
                            )
                        nav_buttons[key] = btn

            def switch_to_page(page_key: str) -> None:
                state["page"] = page_key
                dashboard_panel.set_visibility(page_key == "dashboard")
                tasks_panel.set_visibility(page_key == "tasks")
                calendar_panel.set_visibility(page_key == "calendar")
                analytics_panel.set_visibility(page_key == "analytics")
                if page_key == "dashboard":
                    render_dashboard()
                if page_key == "calendar":
                    render_calendar()
                if page_key == "analytics":
                    render_analytics()
                render_workspace_nav()

            ui.label("SYSTEM").classes(
                "text-xs uppercase tracking-widest text-slate-400 "
                "px-3 mt-7 mb-3 sidebar-hide"
            )
            with ui.column().classes("w-full gap-2"):
                ui.button("Settings", icon="settings").props(
                    "flat no-caps align=left color=grey-8"
                ).classes("w-full px-3 py-2 rounded-lg nav-item")

            with ui.row().classes(
                "items-center gap-3 px-3 pt-4 pb-1 mt-auto "
                "border-t border-slate-200"
            ):
                with ui.element("div").classes(
                    "w-9 h-9 rounded-full bg-teal-600 "
                    "flex items-center justify-center shrink-0"
                ):
                    ui.label("A").classes(
                        "text-white font-semibold text-sm"
                    )
                with ui.column().classes("gap-0 min-w-0 sidebar-hide"):
                    ui.label("Alex C.").classes(
                        "text-sm font-medium text-slate-900"
                    )
                    ui.label("Student").classes(
                        "text-xs text-slate-500"
                    )

    expand_btn = ui.button(icon="chevron_right").props(
        "flat round dense color=grey-7"
    ).classes(
        "fixed top-20 left-2 z-50 bg-white shadow-md rounded-full"
    )
    expand_btn.tooltip("Open sidebar")
    expand_btn.set_visibility(False)
    expand_btn.on("click", toggle_sidebar)

    with ui.header().classes(
        "bg-white items-center px-6 py-3 border-b border-slate-200"
    ).props("flat"):
        with ui.row().classes("items-center flex-1"):
            with ui.row().classes("items-center gap-2"):
                ui.icon("bolt").classes("text-xl text-teal-600")
                ui.label("Bizzy").classes(
                    "text-lg font-semibold tracking-wide text-slate-900"
                )

        with ui.row().classes("items-center justify-center flex-1"):
            global_search_input = ui.input(
                placeholder="Search tasks..."
            ).props("outlined dense clearable").classes("w-full max-w-md")

        with ui.row().classes("items-center gap-3 flex-1 justify-end"):
            create_button = ui.button("New Task", icon="add").props(
                'color=teal-7 unelevated no-caps dense padding="6px 10px"'
            )
            create_button.classes("rounded-lg new-task-btn")
            with ui.row().classes("items-center gap-1"):
                with ui.button(icon="notifications").props(
                    "flat round color=grey-7"
                ):
                    notif_badge = ui.badge("0", color="red").props("floating")
                    notif_badge.set_visibility(False)
                    with ui.menu().props(
                        'anchor="bottom right" self="top right"'
                    ):
                        notif_menu_container = ui.column().classes(
                            "p-3 gap-2 w-72"
                        )
                ui.button(icon="settings").props("flat round color=grey-7")

    with ui.column().classes("w-full gap-4 p-6 mx-auto").style("max-width: 1280px;"):
        dashboard_panel = ui.column().classes("w-full gap-6")

        tasks_panel = ui.column().classes("w-full gap-4")
        tasks_panel.set_visibility(False)
        with tasks_panel:
            with ui.column().classes("gap-1"):
                ui.label("Task management").classes("text-2xl font-semibold text-slate-900")
                subtitle_label = ui.label("0 tasks").classes("text-sm text-slate-500")

            with ui.row().classes("w-full items-center justify-between gap-4"):
                with ui.row().classes("items-center gap-2"):
                    status_select = (
                        ui.select(
                            {"all": "All", "pending": "Pending", "completed": "Completed"},
                            value=state["status"],
                            label="Status",
                        )
                        .props("outlined dense options-dense")
                        .classes("w-36")
                    )
                    priority_select = (
                        ui.select(
                            {
                                "all": "All",
                                "low": "Low",
                                "medium": "Medium",
                                "high": "High",
                            },
                            value=state["priority"],
                            label="Priority",
                        )
                        .props("outlined dense options-dense")
                        .classes("w-32")
                    )
                    category_select = (
                        ui.select(
                            {
                                "all": "All",
                                "Project": "Project",
                                "Exam": "Exam",
                                "Assignment": "Assignment",
                                "Reading": "Reading",
                                "Other": "Other",
                            },
                            value=state["category"],
                            label="Category",
                        )
                        .props("outlined dense options-dense")
                        .classes("w-36")
                    )
                    sort_select = (
                        ui.select(
                            {
                                "due_date": "Due date",
                                "title": "Title",
                                "priority": "Priority",
                                "status": "Status",
                            },
                            value=state["sort"],
                            label="Sort by",
                        )
                        .props("outlined dense options-dense")
                        .classes("w-36")
                    )
                view_toggle = ui.toggle(
                    {"board": "Board", "list": "List"},
                    value=state["view"],
                ).props("unelevated no-caps toggle-color=teal-7")

            status_select.set_visibility(state["view"] == "list")
            sort_select.set_visibility(state["view"] == "list")

            tasks_container = ui.column().classes("w-full")

        calendar_panel = ui.column().classes("w-full gap-4")
        calendar_panel.set_visibility(False)

        analytics_panel = ui.column().classes("w-full gap-6")
        analytics_panel.set_visibility(False)

    def open_task_dialog(task=None, default_due_date: date | None = None) -> None:
        is_edit = task is not None
        button_label = "Save changes" if is_edit else "Save task"
        if is_edit:
            default_due_iso = ""
        elif default_due_date:
            default_due_iso = default_due_date.isoformat()
        else:
            default_due_iso = date.today().isoformat()

        with ui.dialog().props("persistent") as dialog, ui.card().classes(
            "w-[460px] max-w-full rounded-2xl p-6 gap-2"
        ):
            with ui.row().classes("w-full items-center justify-between"):
                ui.label("EDIT TASK" if is_edit else "NEW TASK").classes(
                    "text-xs uppercase tracking-widest text-slate-400"
                )
                close_btn = ui.button(icon="close").props(
                    "flat round dense color=grey-7"
                )
                close_btn.tooltip("Close")
                close_btn.on("click", dialog.close)
            title_input = (
                ui.input(
                    placeholder="What needs to be done?",
                    value=task.title if is_edit else "",
                )
                .props(
                    'borderless autofocus dense hide-bottom-space '
                    'input-class="text-xl"'
                )
                .classes("w-full")
            )

            with ui.row().classes(
                "w-full items-center justify-between flex-wrap"
            ):
                priority_input = (
                    ui.select(
                        {"low": "Low", "medium": "Medium", "high": "High"},
                        value=task.priority.value if is_edit else None,
                        label="Priority",
                    )
                    .props('dense outlined options-dense placeholder="Select..."')
                    .classes("w-32")
                )

                category_input = (
                    ui.select(
                        ["Project", "Exam", "Assignment", "Reading"],
                        value=task.category if is_edit else None,
                        label="Category",
                        with_input=True,
                        new_value_mode="add-unique",
                    )
                    .props(
                        'dense outlined options-dense '
                        'placeholder="Pick or type..."'
                    )
                    .classes("w-28")
                )

                due_date_input = (
                    ui.input(
                        value=(
                            task.due_date.isoformat()
                            if is_edit and task.due_date
                            else default_due_iso
                        ),
                        label="Due date",
                    )
                    .props(
                        'dense outlined type=date '
                        'prepend-icon="event" hide-bottom-space'
                    )
                    .classes("w-32 due-date-input")
                )

                status_input = None
                if is_edit:
                    current_status = (
                        "pending"
                        if task.status.value == "created"
                        else task.status.value
                    )
                    status_input = (
                        ui.select(
                            {
                                "pending": "To do",
                                "in_progress": "In progress",
                                "done": "Done",
                            },
                            value=current_status,
                        )
                        .props("dense outlined options-dense")
                        .classes("w-36")
                    )

            description_input = (
                ui.textarea(
                    placeholder="Add notes, context, or links...",
                    value=task.description if is_edit else "",
                )
                .props("outlined autogrow")
                .classes("w-full")
            )

            add_another_checkbox = None

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
                    not is_edit
                    and add_another_checkbox is not None
                    and add_another_checkbox.value
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
                if state["page"] == "calendar":
                    render_calendar()
                if state["page"] == "dashboard":
                    render_dashboard()
                if state["page"] == "analytics":
                    render_analytics()

            def confirm_delete() -> None:
                with ui.dialog() as confirm_dialog, ui.card().classes(
                    "w-[400px] max-w-full rounded-2xl p-6 gap-3"
                ):
                    ui.label("Delete this task?").classes(
                        "text-lg font-semibold text-slate-900"
                    )
                    ui.label(
                        "This action cannot be undone."
                    ).classes("text-sm text-slate-500")

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
                "w-full items-center justify-between pt-3 mt-1 "
                "border-t border-slate-100"
            ):
                if is_edit:
                    ui.button(
                        "Delete", icon="delete", on_click=confirm_delete
                    ).props("flat color=negative no-caps")
                else:
                    add_another_checkbox = ui.checkbox("Add another")
                with ui.row().classes("gap-2"):
                    ui.button("Cancel", on_click=dialog.close).props(
                        "flat color=grey-7 no-caps"
                    )
                    ui.button(button_label, on_click=save).props(
                        "color=teal-7 unelevated no-caps"
                    )

        dialog.open()

    def render_empty_state() -> None:
        with ui.column().classes("w-full items-center gap-3 px-6 py-12 text-center"):
            ui.icon("inbox", size="3rem").classes("text-slate-300")
            ui.label("No matching tasks").classes("text-lg font-medium text-slate-700")
            ui.label(
                "Create a new task or adjust your filters to see more results."
            ).classes("text-sm text-slate-500")

    def render_list(tasks, on_complete, on_reopen, on_delete) -> None:
        today = date.today()

        with ui.row().classes(
            "w-full items-center gap-4 px-6 py-4 text-xs font-semibold uppercase tracking-wide text-slate-500"
        ):
            ui.label("Task").classes("flex-1 min-w-0")
            ui.label("Priority").classes("w-24")
            ui.label("Status").classes("w-28")
            ui.label("Due").classes("w-44")
            ui.element("div").classes("w-32")

        ui.separator()

        for task in tasks:
            assert task.id is not None
            is_done = task.completed
            is_late = (
                task.due_date is not None
                and not is_done
                and task.due_date < today
            )

            with ui.column().classes("w-full gap-0"):
                row = ui.row().classes(
                    "w-full items-center gap-4 px-6 py-3 cursor-pointer hover:bg-slate-50 transition-colors"
                )
                row.on(
                    "click",
                    lambda current_task=task: open_task_dialog(current_task),
                )
                with row:
                    with ui.column().classes("flex-1 min-w-0 gap-1"):
                        title_classes = "font-medium text-slate-900 truncate w-full"
                        if is_done:
                            title_classes += " line-through text-slate-400"
                        ui.label(task.title).classes(title_classes)
                        with ui.row().classes("items-center gap-2"):
                            ui.label(category_display(task.category)).classes(
                                "text-xs rounded px-2 py-1 "
                                f"{category_pill_class(task.category)}"
                            )
                            if task.description:
                                ui.label("·").classes(
                                    "text-xs text-slate-300"
                                )
                                ui.label(task.description).classes(
                                    "text-xs text-slate-500 truncate"
                                )

                    with ui.element("div").classes("w-24"):
                        ui.badge(
                            task.priority.value.title(),
                            color=get_priority_color(task.priority.value),
                        )
                    with ui.element("div").classes("w-28"):
                        ui.badge(
                            status_display_label(task.status.value),
                            color=get_status_color(task.status.value),
                        )

                    if task.due_date:
                        due_text = relative_due_text(task.due_date, today, is_done)
                        due_classes = (
                            "w-44 text-sm text-red-600 font-medium"
                            if is_late
                            else "w-44 text-sm text-slate-600"
                        )
                    else:
                        due_text = "No due date"
                        due_classes = "w-44 text-sm text-slate-400"
                    ui.label(due_text).classes(due_classes)

                    with ui.row().classes("w-32 justify-end gap-1"):
                        if is_done:
                            reopen_btn = ui.button(icon="undo").props(
                                "flat round dense color=grey-7"
                            )
                            reopen_btn.tooltip("Reopen task")
                            reopen_btn.on(
                                "click.stop",
                                lambda task_id=task.id: on_reopen(task_id),
                            )
                        else:
                            complete_btn = ui.button(icon="check_circle").props(
                                "flat round dense color=positive"
                            )
                            complete_btn.tooltip("Mark complete")
                            complete_btn.on(
                                "click.stop",
                                lambda task_id=task.id: on_complete(task_id),
                            )
                        delete_btn = ui.button(icon="delete").props(
                            "flat round dense color=negative"
                        )
                        delete_btn.tooltip("Delete task")
                        delete_btn.on(
                            "click.stop",
                            lambda task_id=task.id: on_delete(task_id),
                        )

                ui.separator()

    def render_board(tasks, on_complete, on_reopen, on_delete) -> None:
        todo_tasks = [t for t in tasks if t.status.value in ("created", "pending")]
        in_progress_tasks = [t for t in tasks if t.status.value == "in_progress"]
        done_tasks = [t for t in tasks if t.status.value == "done"]

        columns = [
            ("To do", todo_tasks, "bg-slate-400", "text-slate-700", "pending"),
            ("In progress", in_progress_tasks, "bg-blue-500", "text-blue-700", "in_progress"),
            ("Done", done_tasks, "bg-emerald-500", "text-emerald-700", "done"),
        ]

        today = date.today()

        def handle_drop(target_status: str) -> None:
            dragging_id = state.get("dragging")
            if dragging_id is None:
                return
            state["dragging"] = None
            if change_task_status(dragging_id, target_status) is not None:
                refresh_tasks()

        highlight_classes = "!ring-2 !ring-teal-500 !bg-slate-300"

        def enter_column(card, depth) -> None:
            depth["d"] += 1
            if depth["d"] == 1:
                card.classes(add=highlight_classes)

        def leave_column(card, depth) -> None:
            depth["d"] -= 1
            if depth["d"] <= 0:
                depth["d"] = 0
                card.classes(remove=highlight_classes)

        def drop_on_column(card, depth, status) -> None:
            depth["d"] = 0
            card.classes(remove=highlight_classes)
            handle_drop(status)

        with ui.row().classes("w-full items-start gap-4"):
            for column_title, column_tasks, dot_class, text_class, target_status in columns:
                column_card = ui.card().classes(
                    "flex flex-col flex-1 min-w-[280px] rounded-2xl shadow-none p-4 gap-3 !bg-slate-200"
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
                    lambda e=None, c=column_card, d=column_depth, s=target_status: drop_on_column(c, d, s),
                )
                with column_card:
                    with ui.row().classes("w-full items-center gap-2"):
                        ui.element("div").classes(f"w-2 h-2 rounded-full {dot_class}")
                        ui.label(column_title).classes(
                            f"text-sm font-semibold {text_class}"
                        )
                        ui.element("div").classes("grow")
                        ui.label(str(len(column_tasks))).classes(
                            "text-xs font-semibold text-slate-500 bg-slate-100 rounded-full px-2 py-1"
                        )

                    for task in column_tasks:
                        assert task.id is not None
                        is_done = task.completed
                        is_late = (
                            task.due_date is not None
                            and not is_done
                            and task.due_date < today
                        )

                        card = ui.card().classes(
                            "w-full rounded-xl shadow-sm p-3 gap-2 cursor-grab active:cursor-grabbing hover:shadow-md transition-shadow"
                        ).props("draggable=true")
                        card.on(
                            "click",
                            lambda current_task=task: open_task_dialog(current_task),
                        )
                        card.on(
                            "dragstart",
                            lambda e=None, task_id=task.id: state.__setitem__(
                                "dragging", task_id
                            ),
                        )
                        with card:
                            title_classes = "font-medium text-slate-900 truncate w-full"
                            if is_done:
                                title_classes += " line-through text-slate-400"
                            ui.label(task.title).classes(title_classes)

                            with ui.row().classes(
                                "items-center gap-2 flex-wrap"
                            ):
                                ui.label(
                                    category_display(task.category)
                                ).classes(
                                    "text-xs rounded px-2 py-1 "
                                    f"{category_pill_class(task.category)}"
                                )
                                ui.label(
                                    task.priority.value.upper()
                                ).classes(
                                    "text-xs rounded px-2 py-1 "
                                    f"{priority_pill_class(task.priority.value)}"
                                )
                            if task.due_date:
                                due_text = relative_due_text(
                                    task.due_date, today, is_done
                                )
                                due_classes = (
                                    "text-xs text-red-600 font-medium"
                                    if is_late
                                    else "text-xs text-slate-500"
                                )
                                ui.label(due_text).classes(due_classes)

                    if not column_tasks and column_title != "To do":
                        empty_messages = {
                            "In progress": "Nothing in progress",
                            "Done": "No completed tasks yet",
                        }
                        with ui.column().classes(
                            "w-full items-center justify-center py-8 gap-2"
                        ):
                            ui.icon("inbox", size="1.5rem").classes("text-slate-400")
                            ui.label(
                                empty_messages.get(column_title, "No tasks")
                            ).classes("text-xs text-slate-500")

                    if column_title == "To do":
                        add_btn = ui.element("div").classes(
                            "w-full rounded-xl border border-dashed border-slate-300 "
                            "hover:border-slate-400 hover:bg-slate-50 p-3 cursor-pointer "
                            "transition-colors"
                        )
                        with add_btn:
                            with ui.row().classes(
                                "items-center justify-center gap-1 text-slate-500"
                            ):
                                ui.icon("add").classes("text-base")
                                ui.label("Add task").classes("text-sm")
                        add_btn.on("click", lambda: open_task_dialog())

    def navigate_month(delta: int) -> None:
        current = state["view_month"]
        if delta > 0:
            if current.month == 12:
                new_month = current.replace(year=current.year + 1, month=1)
            else:
                new_month = current.replace(month=current.month + 1)
        else:
            if current.month == 1:
                new_month = current.replace(year=current.year - 1, month=12)
            else:
                new_month = current.replace(month=current.month - 1)
        state["view_month"] = new_month
        render_calendar()

    def navigate_to_today() -> None:
        state["view_month"] = date.today().replace(day=1)
        state["selected_date"] = date.today()
        render_calendar()

    def select_date(d: date) -> None:
        if state["calendar_filter_date"] == d:
            state["calendar_filter_date"] = None
        else:
            state["calendar_filter_date"] = d
        state["selected_date"] = d
        if d.year != state["view_month"].year or d.month != state["view_month"].month:
            state["view_month"] = d.replace(day=1)
        render_calendar()

    def clear_calendar_filter() -> None:
        state["calendar_filter_date"] = None
        render_calendar()

    def render_dashboard() -> None:
        dashboard_panel.clear()
        with dashboard_panel:
            all_tasks = get_tasks()
            today = date.today()
            tomorrow = today + timedelta(days=1)
            week_end = today + timedelta(days=7)

            open_tasks = [t for t in all_tasks if not t.completed]
            completed_tasks = [t for t in all_tasks if t.completed]
            overdue = [
                t for t in open_tasks if t.due_date and t.due_date < today
            ]
            due_today = [t for t in open_tasks if t.due_date == today]
            due_tomorrow = [t for t in open_tasks if t.due_date == tomorrow]
            due_rest_of_week = sorted(
                [
                    t
                    for t in open_tasks
                    if t.due_date
                    and today + timedelta(days=2) <= t.due_date <= week_end
                ],
                key=lambda t: t.due_date,
            )

            hour = datetime.now().hour
            if hour < 12:
                greeting_text = "Good morning"
            elif hour < 17:
                greeting_text = "Good afternoon"
            else:
                greeting_text = "Good evening"

            priority_rank = {"high": 0, "medium": 1, "low": 2}
            priority_pill_classes = {
                "low": "bg-emerald-100 text-emerald-700",
                "medium": "bg-amber-100 text-amber-700",
                "high": "bg-rose-100 text-rose-700",
            }

            def dashboard_quick_complete(task_id: int) -> None:
                if complete_task(task_id):
                    refresh_tasks()

            status_pill_classes = {
                "in_progress": "bg-blue-100 text-blue-700",
                "done": "bg-emerald-100 text-emerald-700",
            }

            def render_briefing_row(t, show_done: bool = True) -> None:
                pill_color = priority_pill_classes.get(
                    t.priority.value, "bg-slate-100 text-slate-700"
                )
                is_late = (
                    t.due_date is not None
                    and not t.completed
                    and t.due_date < today
                )
                row = ui.element("div").classes(
                    "w-full rounded-lg border border-slate-100 px-3 py-3 "
                    "cursor-pointer hover:bg-slate-50 transition-colors "
                    "flex items-start gap-3"
                )
                with row:
                    circle = ui.element("div").classes(
                        "w-5 h-5 rounded-full border-2 border-slate-300 "
                        "hover:border-emerald-500 cursor-pointer shrink-0 mt-1"
                    )
                    if show_done:
                        circle.on(
                            "click.stop",
                            lambda task_id=t.id: dashboard_quick_complete(
                                task_id
                            ),
                        )
                    circle.tooltip("Mark complete")

                    with ui.column().classes("flex-1 min-w-0 gap-2"):
                        title_classes = (
                            "text-sm font-semibold text-slate-900 truncate"
                        )
                        if t.completed:
                            title_classes += " line-through opacity-60"
                        ui.label(t.title).classes(title_classes)
                        with ui.row().classes("items-center gap-2 flex-wrap"):
                            ui.label(category_display(t.category)).classes(
                                "text-xs rounded px-2 py-1 "
                                f"{category_pill_class(t.category)}"
                            )
                            ui.label(t.priority.value.upper()).classes(
                                f"text-xs rounded px-2 py-1 {pill_color}"
                            )
                            if t.status.value in status_pill_classes:
                                status_color = status_pill_classes[
                                    t.status.value
                                ]
                                ui.label(
                                    status_display_label(t.status.value)
                                ).classes(
                                    f"text-xs rounded px-2 py-1 "
                                    f"{status_color}"
                                )
                        if t.due_date:
                            due_text = relative_due_text(
                                t.due_date, today, t.completed
                            )
                            due_classes = (
                                "text-xs text-red-600 font-medium"
                                if is_late
                                else "text-xs text-slate-500"
                            )
                            ui.label(due_text).classes(due_classes)
                row.on("click", lambda task=t: open_task_dialog(task))

            week_count = (
                len(due_today)
                + len(due_tomorrow)
                + len(due_rest_of_week)
            )

            attention_count = len(overdue) + len(due_today)
            if attention_count == 0:
                attention_msg = "nothing urgent today"
            else:
                plural = "s" if attention_count != 1 else ""
                attention_msg = (
                    f"{attention_count} item{plural} needs attention"
                )
            hero_subtitle = (
                f"{today.strftime('%a %d %b')} · {attention_msg}"
            )

            category_progress: list[tuple[str, int]] = []
            cats_seen = set()
            for t in all_tasks:
                key = (t.category or "").strip()
                if not key or key.lower() in cats_seen:
                    continue
                cats_seen.add(key.lower())
                cat_tasks = [
                    x
                    for x in all_tasks
                    if (x.category or "").lower() == key.lower()
                ]
                if not cat_tasks:
                    continue
                pct = round(
                    sum(1 for x in cat_tasks if x.completed)
                    / len(cat_tasks)
                    * 100
                )
                category_progress.append((category_display(key), pct))
            category_progress = sorted(
                category_progress, key=lambda x: -x[1]
            )[:3]

            overall_pct = (
                round(len(completed_tasks) / len(all_tasks) * 100)
                if all_tasks
                else 0
            )

            upcoming_tasks = sorted(
                [
                    t
                    for t in open_tasks
                    if t.due_date and t.due_date >= today
                ],
                key=lambda t: (
                    t.due_date or date.max,
                    priority_rank.get(t.priority.value, 99),
                    t.title.lower(),
                ),
            )

            with ui.element("div").classes(
                "w-full grid grid-cols-3 gap-4"
            ):
                with ui.card().classes(
                    "col-span-2 rounded-2xl !p-6 gap-2 "
                    "!bg-emerald-900 !text-white shadow-none"
                ):
                    ui.label(f"{greeting_text},").classes(
                        "text-2xl font-semibold leading-tight !text-white"
                    )
                    ui.label("Alex.").classes(
                        "text-2xl font-semibold leading-tight !text-white"
                    )
                    ui.label(hero_subtitle).classes(
                        "text-sm text-emerald-200 mt-2"
                    )

                with ui.card().classes(
                    "rounded-2xl !p-5 gap-1 !bg-white shadow-none"
                ):
                    ui.label(str(len(open_tasks))).classes(
                        "text-3xl font-semibold text-slate-900 leading-none"
                    )
                    ui.label("OPEN").classes(
                        "text-xs uppercase tracking-widest text-slate-500 mt-2"
                    )

                with ui.card().classes(
                    "rounded-2xl !p-5 gap-1 !bg-emerald-100 shadow-none"
                ):
                    ui.label(str(len(completed_tasks))).classes(
                        "text-3xl font-semibold text-emerald-900 leading-none"
                    )
                    ui.label("DONE").classes(
                        "text-xs uppercase tracking-widest "
                        "text-emerald-800 mt-2"
                    )

                with ui.card().classes(
                    "rounded-2xl !p-5 gap-1 !bg-orange-100 shadow-none"
                ):
                    ui.label(str(len(overdue))).classes(
                        "text-3xl font-semibold text-orange-900 leading-none"
                    )
                    ui.label("OVERDUE").classes(
                        "text-xs uppercase tracking-widest "
                        "text-orange-800 mt-2"
                    )

                with ui.card().classes(
                    "row-span-2 rounded-2xl !p-6 gap-3 !bg-emerald-900 "
                    "!text-white shadow-none"
                ):
                    ui.label("PROGRESS").classes(
                        "text-xs uppercase tracking-widest text-emerald-200"
                    )
                    for cat_label, pct in category_progress:
                        with ui.row().classes(
                            "w-full items-center justify-between"
                        ):
                            ui.label(cat_label).classes(
                                "text-sm !text-white"
                            )
                            ui.label(f"{pct}%").classes(
                                "text-sm text-emerald-200"
                            )
                        track = ui.element("div").classes(
                            "w-full h-1 rounded-full bg-emerald-800 "
                            "overflow-hidden"
                        )
                        with track:
                            ui.element("div").classes(
                                "h-full bg-emerald-300 rounded-full"
                            ).style(f"width: {pct}%;")
                    with ui.row().classes(
                        "w-full items-center justify-between mt-2"
                    ):
                        ui.label("Overall").classes(
                            "text-sm font-semibold !text-white"
                        )
                        ui.label(f"{overall_pct}%").classes(
                            "text-sm font-semibold text-emerald-200"
                        )
                    track = ui.element("div").classes(
                        "w-full h-1 rounded-full bg-emerald-800 "
                        "overflow-hidden"
                    )
                    with track:
                        ui.element("div").classes(
                            "h-full bg-emerald-300 rounded-full"
                        ).style(f"width: {overall_pct}%;")

                with ui.card().classes(
                    "col-span-2 rounded-2xl !p-5 gap-2 "
                    "!bg-white shadow-none"
                ):
                    ui.label("UPCOMING").classes(
                        "text-xs uppercase tracking-widest text-slate-500"
                    )
                    if not upcoming_tasks:
                        with ui.column().classes(
                            "w-full items-center gap-2 py-6"
                        ):
                            ui.icon("event_available", size="2rem").classes(
                                "text-slate-300"
                            )
                            ui.label("Nothing upcoming").classes(
                                "text-sm font-semibold text-slate-700"
                            )
                    else:
                        for t in upcoming_tasks[:4]:
                            render_briefing_row(t)
                        if len(upcoming_tasks) > 4:
                            ui.label(
                                f"+ {len(upcoming_tasks) - 4} more"
                            ).classes("text-xs text-slate-400 pt-1")

    def render_analytics() -> None:
        analytics_panel.clear()
        with analytics_panel:
            all_tasks = get_tasks()
            today = date.today()
            total = len(all_tasks)

            open_tasks = [t for t in all_tasks if not t.completed]
            completed_tasks = [t for t in all_tasks if t.completed]
            overdue = [t for t in open_tasks if t.due_date and t.due_date < today]
            week_end = today + timedelta(days=7)
            due_this_week = [
                t
                for t in open_tasks
                if t.due_date and today <= t.due_date <= week_end
            ]

            completion_pct = (
                round(len(completed_tasks) / total * 100) if total else 0
            )
            tasks_with_due = [t for t in completed_tasks if t.due_date]
            on_time_done = [
                t for t in tasks_with_due if t.due_date and t.due_date >= today
            ]
            on_time_pct = (
                round(len(on_time_done) / len(tasks_with_due) * 100)
                if tasks_with_due
                else 0
            )

            high_open = sum(
                1 for t in open_tasks if t.priority.value == "high"
            )
            medium_open = sum(
                1 for t in open_tasks if t.priority.value == "medium"
            )
            low_open = sum(
                1 for t in open_tasks if t.priority.value == "low"
            )
            pending_total = high_open + medium_open + low_open

            with ui.row().classes("w-full items-center justify-between gap-4"):
                with ui.column().classes("gap-1"):
                    ui.label("Analytics").classes(
                        "text-2xl font-semibold text-slate-900"
                    )
                    ui.label(
                        f"Insights across {total} task"
                        f"{'s' if total != 1 else ''}"
                    ).classes("text-sm text-slate-500")

            kpi_cards = [
                (
                    "Completion rate",
                    f"{completion_pct}%",
                    f"{len(completed_tasks)} of {total} done",
                    "text-emerald-600",
                ),
                (
                    "On-time rate",
                    f"{on_time_pct}%",
                    f"{len(on_time_done)} of {len(tasks_with_due)} on time"
                    if tasks_with_due
                    else "No dated completions yet",
                    "text-teal-600",
                ),
                (
                    "Active",
                    str(len(open_tasks)),
                    f"{len(overdue)} overdue",
                    "text-slate-900",
                ),
                (
                    "Due this week",
                    str(len(due_this_week)),
                    "Next 7 days",
                    "text-amber-600",
                ),
            ]
            with ui.row().classes("w-full gap-3 flex-nowrap"):
                for label, value, sub, accent in kpi_cards:
                    with ui.card().classes(
                        "flex-1 min-w-0 rounded-xl shadow-sm !p-3 gap-0"
                    ):
                        ui.label(label).classes(
                            "text-xs uppercase tracking-widest text-slate-500"
                        )
                        ui.label(value).classes(
                            f"text-2xl font-semibold {accent} leading-tight"
                        )
                        ui.label(sub).classes("text-xs text-slate-500")

            with ui.row().classes("w-full items-stretch gap-4 flex-nowrap"):
                with ui.card().classes(
                    "flex-1 min-w-0 rounded-2xl shadow-sm !p-5 gap-3"
                ):
                    ui.label("Due-date heatmap").classes(
                        "text-lg font-semibold text-slate-900"
                    )
                    ui.label("Next 12 weeks · darker = more tasks due").classes(
                        "text-sm text-slate-400"
                    )

                    weeks_count = 12
                    week_start = today - timedelta(days=today.weekday())
                    horizon_end = week_start + timedelta(weeks=weeks_count) - timedelta(days=1)

                    due_counts: dict[date, int] = {}
                    for t in open_tasks:
                        if t.due_date and week_start <= t.due_date <= horizon_end:
                            due_counts[t.due_date] = due_counts.get(t.due_date, 0) + 1

                    def color_for(count: int) -> str:
                        if count == 0:
                            return "bg-slate-100"
                        if count == 1:
                            return "bg-teal-200"
                        if count == 2:
                            return "bg-teal-400"
                        if count == 3:
                            return "bg-teal-600"
                        return "bg-teal-800"

                    if not due_counts:
                        with ui.column().classes(
                            "w-full items-center gap-2 py-8"
                        ):
                            ui.icon("event_busy", size="2rem").classes(
                                "text-slate-300"
                            )
                            ui.label("No upcoming due dates").classes(
                                "text-sm text-slate-500"
                            )
                    else:
                        with ui.row().classes(
                            "items-start gap-2 mt-3 w-full overflow-x-auto"
                        ):
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
                                    ui.label(d_label).classes(
                                        "text-xs text-slate-400 h-5 leading-5"
                                    )

                            with ui.element("div").classes(
                                "grid grid-flow-col grid-rows-7 gap-1 shrink-0"
                            ):
                                for w in range(weeks_count):
                                    column_start = week_start + timedelta(weeks=w)
                                    for day_offset in range(7):
                                        d = column_start + timedelta(
                                            days=day_offset
                                        )
                                        count = due_counts.get(d, 0)
                                        cell = ui.element("div").classes(
                                            f"w-5 h-5 rounded "
                                            f"{color_for(count)} "
                                            "cursor-default"
                                        )
                                        plural = "s" if count != 1 else ""
                                        cell.tooltip(
                                            f"{d.strftime('%a %b %d')}: "
                                            f"{count} task{plural}"
                                            if count
                                            else d.strftime("%a %b %d")
                                        )

                        with ui.row().classes(
                            "w-full items-center gap-2 mt-3"
                        ):
                            ui.label("Less").classes("text-xs text-slate-400")
                            for level_class in [
                                "bg-slate-100",
                                "bg-teal-200",
                                "bg-teal-400",
                                "bg-teal-600",
                                "bg-teal-800",
                            ]:
                                ui.element("div").classes(
                                    f"w-3 h-3 rounded {level_class}"
                                )
                            ui.label("More").classes("text-xs text-slate-400")

                with ui.card().classes(
                    "flex-1 min-w-0 rounded-2xl shadow-sm !p-5 gap-1"
                ):
                    ui.label("Priority mix").classes(
                        "text-lg font-semibold text-slate-900"
                    )
                    ui.label("All pending tasks").classes(
                        "text-sm text-slate-400"
                    )

                    if pending_total == 0:
                        with ui.column().classes(
                            "w-full items-center gap-2 py-10"
                        ):
                            ui.icon("celebration", size="2rem").classes(
                                "text-emerald-400"
                            )
                            ui.label("No pending tasks").classes(
                                "text-sm text-slate-500"
                            )
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
                                            "name": "Priority",
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
                                                    "value": high_open,
                                                    "name": "High",
                                                    "itemStyle": {
                                                        "color": "#EF4444"
                                                    },
                                                },
                                                {
                                                    "value": medium_open,
                                                    "name": "Medium",
                                                    "itemStyle": {
                                                        "color": "#F59E0B"
                                                    },
                                                },
                                                {
                                                    "value": low_open,
                                                    "name": "Low",
                                                    "itemStyle": {
                                                        "color": "#10B981"
                                                    },
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
                                ui.label(str(pending_total)).classes(
                                    "text-4xl font-semibold text-slate-900"
                                )
                                ui.label("PENDING").classes(
                                    "text-xs font-semibold "
                                    "text-slate-500 tracking-widest mt-1"
                                )

                        with ui.row().classes(
                            "w-full items-center justify-center "
                            "gap-5 mt-3 flex-wrap"
                        ):
                            for label, count, color_class in [
                                ("High", high_open, "bg-red-500"),
                                ("Med", medium_open, "bg-amber-500"),
                                ("Low", low_open, "bg-emerald-500"),
                            ]:
                                with ui.row().classes("items-center gap-2"):
                                    ui.element("div").classes(
                                        f"w-2.5 h-2.5 rounded-full {color_class}"
                                    )
                                    ui.label(f"{count} {label}").classes(
                                        "text-sm font-medium text-slate-700"
                                    )

    def render_calendar() -> None:
        calendar_panel.clear()
        with calendar_panel:
            view_month = state["view_month"]
            today = date.today()
            selected = state["selected_date"]
            all_tasks = get_tasks()

            tasks_by_date: dict = {}
            for t in all_tasks:
                if t.due_date:
                    tasks_by_date.setdefault(t.due_date, []).append(t)

            month_start = view_month
            if view_month.month == 12:
                month_end = view_month.replace(
                    year=view_month.year + 1, month=1
                ) - timedelta(days=1)
            else:
                month_end = view_month.replace(
                    month=view_month.month + 1
                ) - timedelta(days=1)
            month_open_count = sum(
                1
                for t in all_tasks
                if t.due_date
                and not t.completed
                and month_start <= t.due_date <= month_end
            )

            upcoming_tasks = sorted(
                [
                    t
                    for t in all_tasks
                    if t.due_date and not t.completed
                ],
                key=lambda t: t.due_date,
            )

            with ui.row().classes(
                "w-full items-center justify-between gap-4"
            ):
                with ui.column().classes("gap-1"):
                    ui.label(view_month.strftime("%B %Y")).classes(
                        "text-2xl font-semibold text-emerald-900"
                    )
                    plural = "s" if month_open_count != 1 else ""
                    ui.label(
                        f"{month_open_count} task{plural} due this month"
                    ).classes("text-sm text-slate-500")
                with ui.row().classes("items-center gap-1"):
                    today_btn = ui.button("Today").props(
                        "flat dense no-caps color=teal-7"
                    )
                    today_btn.on("click", navigate_to_today)
                    prev_btn = ui.button(icon="chevron_left").props(
                        "flat round dense color=grey-7"
                    )
                    prev_btn.on("click", lambda: navigate_month(-1))
                    next_btn = ui.button(icon="chevron_right").props(
                        "flat round dense color=grey-7"
                    )
                    next_btn.on("click", lambda: navigate_month(1))

            with ui.row().classes(
                "w-full items-stretch gap-4 flex-nowrap"
            ):
                with ui.card().classes(
                    "flex-1 min-w-0 rounded-2xl !p-5 gap-3 "
                    "!bg-white shadow-none"
                ):
                    with ui.element("div").classes(
                        "w-full grid grid-cols-7 gap-1 mb-1"
                    ):
                        for day_label in [
                            "Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"
                        ]:
                            ui.label(day_label).classes(
                                "text-xs text-slate-400 text-center"
                            )

                    cal = cal_module.Calendar(firstweekday=0)
                    month_dates = list(
                        cal.itermonthdates(
                            view_month.year, view_month.month
                        )
                    )

                    with ui.element("div").classes(
                        "w-full grid grid-cols-7 gap-1"
                    ):
                        for d in month_dates:
                            is_current_month = d.month == view_month.month
                            is_today_cell = d == today
                            is_selected = d == selected

                            if not is_current_month:
                                ui.element("div").classes("h-20")
                                continue

                            cell_tasks_all = tasks_by_date.get(d, [])
                            cell_tasks_open = [
                                t for t in cell_tasks_all if not t.completed
                            ]
                            has_tasks = bool(cell_tasks_open)
                            is_overdue_day = (
                                has_tasks and d < today
                            )

                            cell_classes = (
                                "h-20 rounded-xl flex flex-col "
                                "items-center justify-center cursor-pointer "
                                "transition-colors relative"
                            )
                            if is_selected:
                                cell_classes += (
                                    " ring-2 ring-emerald-700 bg-emerald-50"
                                )
                            elif is_today_cell:
                                cell_classes += " bg-emerald-100"
                            else:
                                cell_classes += (
                                    " bg-stone-50 hover:bg-stone-100"
                                )

                            cell = ui.element("div").classes(cell_classes)
                            cell.on(
                                "click", lambda day=d: select_date(day)
                            )
                            with cell:
                                num_classes = "text-sm "
                                if is_today_cell or is_selected:
                                    num_classes += (
                                        "font-semibold text-emerald-900"
                                    )
                                else:
                                    num_classes += "text-slate-700"
                                ui.label(str(d.day)).classes(num_classes)
                                if has_tasks:
                                    dot_color = (
                                        "bg-rose-500"
                                        if is_overdue_day
                                        else "bg-emerald-600"
                                    )
                                    ui.element("div").classes(
                                        f"absolute bottom-1 w-1 h-1 "
                                        f"rounded-full {dot_color}"
                                    )

                with ui.card().classes(
                    "w-80 shrink-0 rounded-2xl !p-5 gap-3 "
                    "!bg-white shadow-none"
                ):
                    filter_date = state["calendar_filter_date"]
                    if filter_date:
                        panel_tasks = sorted(
                            tasks_by_date.get(filter_date, []),
                            key=lambda t: (
                                t.completed,
                                PRIORITY_RANK.get(t.priority.value, 99),
                                t.title.lower(),
                            ),
                        )
                        header_label = filter_date.strftime(
                            "%a %d %b"
                        ).upper()
                    else:
                        panel_tasks = upcoming_tasks
                        header_label = "UPCOMING"

                    with ui.row().classes(
                        "w-full items-center justify-between"
                    ):
                        ui.label(header_label).classes(
                            "text-xs uppercase tracking-widest text-slate-500"
                        )
                        if filter_date:
                            clear_btn = ui.button("Show all").props(
                                "flat dense no-caps color=teal-7"
                            )
                            clear_btn.on(
                                "click", clear_calendar_filter
                            )

                    if not panel_tasks:
                        with ui.column().classes(
                            "w-full items-center gap-2 py-6"
                        ):
                            ui.icon("event_available", size="2rem").classes(
                                "text-slate-300"
                            )
                            empty_text = (
                                "No tasks this day"
                                if filter_date
                                else "Nothing upcoming"
                            )
                            ui.label(empty_text).classes(
                                "text-sm text-slate-500"
                            )
                    else:
                        for t in panel_tasks[:8]:
                            is_late = (
                                t.due_date is not None
                                and not t.completed
                                and t.due_date < today
                            )
                            days_diff = (
                                (t.due_date - today).days
                                if t.due_date
                                else 0
                            )
                            if is_late:
                                hint_color = "text-rose-600"
                                border_color = "border-rose-500"
                                hint_text = (
                                    f"{t.due_date.strftime('%d %b')} · "
                                    f"{-days_diff}d overdue"
                                )
                            elif t.completed:
                                hint_color = "text-slate-400"
                                border_color = "border-slate-300"
                                hint_text = (
                                    f"{t.due_date.strftime('%d %b')} · done"
                                )
                            else:
                                hint_color = "text-slate-500"
                                border_color = "border-emerald-700"
                                if days_diff == 0:
                                    hint_text = (
                                        f"{t.due_date.strftime('%d %b')} "
                                        "· today"
                                    )
                                else:
                                    hint_text = (
                                        f"{t.due_date.strftime('%d %b')} "
                                        f"· in {days_diff}d"
                                    )
                            item = ui.element("div").classes(
                                "w-full pl-3 py-1 cursor-pointer "
                                f"border-l-4 {border_color} "
                                "hover:bg-stone-50 transition-colors"
                            )
                            with item:
                                title_classes = (
                                    "text-sm font-semibold text-slate-900 "
                                    "truncate"
                                )
                                if t.completed:
                                    title_classes += (
                                        " line-through opacity-60"
                                    )
                                ui.label(t.title).classes(title_classes)
                                ui.label(hint_text).classes(
                                    f"text-xs {hint_color}"
                                )
                            item.on(
                                "click",
                                lambda task=t: open_task_dialog(task),
                            )

                        if len(panel_tasks) > 8:
                            ui.label(
                                f"+ {len(panel_tasks) - 8} more"
                            ).classes("text-xs text-slate-400 pt-2")

                    if filter_date:
                        add_label = (
                            f"+ Add task to {filter_date.strftime('%d %b')}"
                        )
                        add_btn = ui.element("div").classes(
                            "w-full rounded-xl border border-dashed "
                            "border-slate-300 hover:border-slate-400 "
                            "hover:bg-stone-50 p-3 cursor-pointer "
                            "transition-colors mt-2 text-center"
                        )
                        with add_btn:
                            ui.label(add_label).classes(
                                "text-sm text-slate-500"
                            )
                        add_btn.on(
                            "click",
                            lambda: open_task_dialog(
                                default_due_date=filter_date
                            ),
                        )

    def notification_quick_complete(task_id: int) -> None:
        if complete_task(task_id):
            refresh_tasks()

    def render_notifications() -> None:
        notif_menu_container.clear()
        all_tasks = get_tasks()
        today = date.today()
        tomorrow = today + timedelta(days=1)

        open_tasks = [t for t in all_tasks if not t.completed]

        notifications = []
        for t in open_tasks:
            if t.due_date and t.due_date < today:
                days_late = (today - t.due_date).days
                plural = "s" if days_late != 1 else ""
                notifications.append(
                    (
                        t,
                        f"Overdue · {days_late} day{plural} late",
                        "schedule",
                        "bg-rose-100",
                        "text-rose-700",
                        0,
                    )
                )
            elif t.due_date == today:
                notifications.append(
                    (
                        t,
                        "Due today",
                        "today",
                        "bg-amber-100",
                        "text-amber-700",
                        1,
                    )
                )
            elif t.due_date == tomorrow:
                notifications.append(
                    (
                        t,
                        "Due tomorrow",
                        "event",
                        "bg-teal-100",
                        "text-teal-700",
                        2,
                    )
                )
            elif t.priority.value == "high" and t.due_date is None:
                notifications.append(
                    (
                        t,
                        "High priority · no due date",
                        "priority_high",
                        "bg-slate-100",
                        "text-slate-700",
                        3,
                    )
                )

        notifications.sort(key=lambda x: (x[5], x[0].title.lower()))

        total_count = len(notifications)

        if total_count == 0:
            notif_badge.set_visibility(False)
        else:
            notif_badge.set_visibility(True)
            notif_badge.set_text(str(total_count))

        max_show = 8

        with notif_menu_container:
            with ui.row().classes(
                "w-full items-center justify-between px-1 pt-1"
            ):
                ui.label("Notifications").classes(
                    "text-xs uppercase tracking-widest text-slate-500"
                )
                if total_count:
                    ui.label(f"{total_count} item{'s' if total_count != 1 else ''}").classes(
                        "text-xs text-slate-400"
                    )

            if not notifications:
                with ui.column().classes("w-full items-center gap-2 py-6"):
                    ui.icon("notifications_off", size="1.75rem").classes(
                        "text-slate-300"
                    )
                    ui.label("You're all caught up").classes(
                        "text-sm font-medium text-slate-700"
                    )
                return

            for t, sub_label, icon, bg_class, text_class, _ in notifications[
                :max_show
            ]:
                row = ui.element("div").classes(
                    "w-full rounded-lg px-2 py-2 hover:bg-slate-50 "
                    "cursor-pointer transition-colors flex items-center gap-3"
                )
                with row:
                    with ui.element("div").classes(
                        f"w-8 h-8 rounded-full {bg_class} "
                        "flex items-center justify-center shrink-0"
                    ):
                        ui.icon(icon, size="1rem").classes(text_class)

                    with ui.column().classes("flex-1 min-w-0 gap-0"):
                        ui.label(t.title).classes(
                            "text-sm font-medium text-slate-900 truncate"
                        )
                        ui.label(sub_label).classes(
                            f"text-xs {text_class}"
                        )

                    done_btn = ui.button(icon="check").props(
                        "flat round dense color=positive size=sm"
                    )
                    done_btn.tooltip("Mark complete")
                    done_btn.on(
                        "click.stop",
                        lambda task_id=t.id: notification_quick_complete(
                            task_id
                        ),
                    )

                row.on("click", lambda task=t: open_task_dialog(task))

            if total_count > max_show:
                ui.label(f"+ {total_count - max_show} more").classes(
                    "text-xs text-slate-400 px-2 pt-1"
                )

    def refresh_tasks() -> None:
        tasks_container.clear()

        all_tasks = get_tasks()
        open_count = sum(1 for t in all_tasks if not t.completed)
        completed_count = sum(1 for t in all_tasks if t.completed)

        render_notifications()

        subtitle_label.set_text(
            f"{len(all_tasks)} tasks · {open_count} open · {completed_count} done"
        )

        visible_tasks = list(all_tasks)
        if state["status"] == "pending":
            visible_tasks = [t for t in visible_tasks if not t.completed]
        elif state["status"] == "completed":
            visible_tasks = [t for t in visible_tasks if t.completed]
        if state["priority"] != "all":
            visible_tasks = [t for t in visible_tasks if t.priority.value == state["priority"]]
        if state["category"] != "all":
            visible_tasks = [
                t for t in visible_tasks if t.category == state["category"]
            ]

        query = state["search"]
        if query:
            visible_tasks = [t for t in visible_tasks if query in t.title.lower()]

        priority_order = {"high": 0, "medium": 1, "low": 2}
        status_order = {"created": 0, "pending": 1, "in_progress": 2, "done": 3}
        sort_key = state["sort"]
        if sort_key == "due_date":
            visible_tasks.sort(key=lambda t: t.due_date or date.max)
        elif sort_key == "title":
            visible_tasks.sort(key=lambda t: t.title.lower())
        elif sort_key == "priority":
            visible_tasks.sort(key=lambda t: priority_order.get(t.priority.value, 99))
        elif sort_key == "status":
            visible_tasks.sort(key=lambda t: status_order.get(t.status.value, 99))

        def handle_reopen(task_id: int) -> None:
            if mark_task_pending(task_id):
                refresh_tasks()

        def handle_complete(task_id: int) -> None:
            if complete_task(task_id):
                refresh_tasks()

        def handle_delete(task_id: int) -> None:
            if delete_task(task_id):
                refresh_tasks()

        with tasks_container:
            if not all_tasks:
                with ui.column().classes("w-full items-center gap-3 py-16"):
                    ui.icon("celebration", size="3rem").classes("text-teal-500")
                    ui.label("Welcome to Bizzy").classes(
                        "text-xl font-semibold text-slate-900"
                    )
                    ui.label("Create your first task to get started.").classes(
                        "text-sm text-slate-500"
                    )
                    welcome_btn = ui.button("New task", icon="add").props(
                        "color=teal-7 unelevated no-caps"
                    )
                    welcome_btn.on("click", lambda: open_task_dialog())
                return

            if not visible_tasks:
                render_empty_state()
                return

            if state["view"] == "board":
                render_board(visible_tasks, handle_complete, handle_reopen, handle_delete)
            else:
                with ui.card().classes("w-full rounded-2xl shadow-sm"):
                    render_list(visible_tasks, handle_complete, handle_reopen, handle_delete)

    create_button.on("click", lambda: open_task_dialog())
    status_select.on_value_change(
        lambda e: (state.__setitem__("status", e.value), refresh_tasks())
    )
    priority_select.on_value_change(
        lambda e: (state.__setitem__("priority", e.value), refresh_tasks())
    )
    category_select.on_value_change(
        lambda e: (state.__setitem__("category", e.value), refresh_tasks())
    )
    sort_select.on_value_change(
        lambda e: (state.__setitem__("sort", e.value), refresh_tasks())
    )
    global_search_input.on_value_change(
        lambda e: (state.__setitem__("search", normalize_query(e.value)), refresh_tasks())
    )

    def on_view_change(e) -> None:
        state["view"] = e.value
        status_select.set_visibility(e.value == "list")
        sort_select.set_visibility(e.value == "list")
        refresh_tasks()

    view_toggle.on_value_change(on_view_change)

    render_workspace_nav()
    refresh_tasks()
    render_dashboard()
