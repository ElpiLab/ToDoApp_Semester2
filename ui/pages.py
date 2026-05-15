import calendar as cal_module
from datetime import date

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
    ui.query("body").classes("bg-slate-100")
    ui.query(".q-layout").props('view="LHh LpR fFf"')

    state = {
        "status": "all",
        "priority": "all",
        "sort": "due_date",
        "search": "",
        "view": "board",
        "dragging": None,
        "page": "tasks",
        "view_month": date.today().replace(day=1),
        "selected_date": date.today(),
    }

    with ui.left_drawer(
        value=True, top_corner=True, bottom_corner=True
    ).classes("bg-slate-900 text-white").props("width=260"):
        with ui.column().classes("w-full h-full pt-2 px-4 pb-4 gap-0"):
            with ui.row().classes("items-center gap-2 px-2 py-1"):
                ui.icon("bolt").classes("text-2xl text-teal-400")
                ui.label("Bizzy").classes("text-2xl font-bold tracking-wide")
            ui.separator().classes("bg-slate-700 -mx-4")

            ui.label("WORKSPACE").classes(
                "text-xs uppercase tracking-widest text-slate-500 px-3 mt-5 mb-2"
            )
            workspace_nav_container = ui.column().classes("w-full gap-1")
            nav_buttons: dict = {}

            def render_workspace_nav() -> None:
                workspace_nav_container.clear()
                with workspace_nav_container:
                    workspace_items = [
                        ("Dashboard", "dashboard", "dashboard"),
                        ("Tasks", "task_alt", "tasks"),
                        ("Calendar", "calendar_month", "calendar"),
                        ("Modules", "library_books", "modules"),
                        ("Analytics", "analytics", "analytics"),
                    ]
                    for label, icon, key in workspace_items:
                        is_active = state["page"] == key
                        item_classes = "w-full px-3 py-2 rounded-lg"
                        if is_active:
                            btn = (
                                ui.button(label, icon=icon)
                                .props("flat no-caps align=left color=white")
                                .classes(f"{item_classes} bg-teal-600")
                            )
                        else:
                            btn = (
                                ui.button(label, icon=icon)
                                .props("flat no-caps align=left color=grey-4")
                                .classes(item_classes)
                            )
                        if key in ("tasks", "calendar"):
                            btn.on(
                                "click", lambda k=key: switch_to_page(k)
                            )
                        nav_buttons[key] = btn

            def switch_to_page(page_key: str) -> None:
                state["page"] = page_key
                tasks_panel.set_visibility(page_key == "tasks")
                calendar_panel.set_visibility(page_key == "calendar")
                if page_key == "calendar":
                    render_calendar()
                render_workspace_nav()

            ui.label("SYSTEM").classes(
                "text-xs uppercase tracking-widest text-slate-500 px-3 mt-6 mb-2"
            )
            with ui.column().classes("w-full gap-1"):
                ui.button("Settings", icon="settings").props(
                    "flat no-caps align=left color=grey-4"
                ).classes("w-full px-3 py-2 rounded-lg")

            with ui.row().classes(
                "items-center gap-3 px-2 pt-4 mt-auto border-t border-slate-700"
            ):
                with ui.element("div").classes(
                    "w-9 h-9 rounded-full bg-teal-600 flex items-center justify-center shrink-0"
                ):
                    ui.label("A").classes("text-white font-semibold text-sm")
                ui.label("Alex C.").classes("text-sm font-medium text-white")

    with ui.header().classes(
        "bg-white items-center justify-end px-6 py-3 shadow-sm gap-3"
    ):
        global_search_input = ui.input(
            placeholder="Search assignments, courses..."
        ).props("outlined dense clearable").classes("w-80")
        create_button = ui.button("New Task", icon="add").props(
            "color=teal-7 unelevated"
        )
        create_button.classes("rounded-lg px-4")
        with ui.button(icon="notifications").props("flat round color=grey-7"):
            with ui.menu().props('anchor="bottom right" self="top right"'):
                with ui.column().classes("p-4 gap-2 w-64 items-center"):
                    ui.icon("notifications_off", size="2rem").classes(
                        "text-slate-300"
                    )
                    ui.label("No notifications yet").classes(
                        "text-sm font-medium text-slate-700"
                    )
                    ui.label("You're all caught up.").classes(
                        "text-xs text-slate-400"
                    )
        ui.button(icon="settings").props("flat round color=grey-7")

    with ui.column().classes("w-full gap-4 p-6").style("max-width: 1280px; margin: 0 auto;"):
        tasks_panel = ui.column().classes("w-full gap-4")
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

            tasks_container = ui.column().classes("w-full")

        calendar_panel = ui.column().classes("w-full gap-4")
        calendar_panel.set_visibility(False)

    def open_task_dialog(task=None, default_due_date: date | None = None) -> None:
        is_edit = task is not None
        button_label = "Save changes" if is_edit else "Save task"
        default_due_iso = (
            default_due_date.isoformat() if default_due_date and not is_edit else ""
        )

        with ui.dialog() as dialog, ui.card().classes(
            "w-[480px] max-w-full rounded-2xl p-6 gap-3"
        ):
            ui.label("EDIT TASK" if is_edit else "NEW TASK").classes(
                "text-xs uppercase tracking-widest text-slate-400"
            )
            title_input = (
                ui.input(
                    placeholder="What needs to be done?",
                    value=task.title if is_edit else "",
                )
                .props('borderless autofocus input-class="text-xl"')
                .classes("w-full")
            )

            with ui.row().classes("w-full items-center gap-2 flex-wrap"):
                priority_input = (
                    ui.select(
                        {"low": "Low", "medium": "Medium", "high": "High"},
                        value=task.priority.value if is_edit else "medium",
                    )
                    .props("dense outlined options-dense")
                    .classes("w-32")
                )

                due_date_input = (
                    ui.input(
                        value=(
                            task.due_date.isoformat()
                            if is_edit and task.due_date
                            else default_due_iso
                        ),
                    )
                    .props("dense outlined type=date")
                    .classes("w-40")
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

            description_section = ui.expansion(
                "Add description",
                icon="notes",
                value=is_edit and bool(task.description),
            ).classes("w-full")
            with description_section:
                description_input = (
                    ui.textarea(
                        placeholder="Add notes, context, or links...",
                        value=task.description if is_edit else "",
                    )
                    .props("outlined autogrow borderless")
                    .classes("w-full")
                )

            add_another_checkbox = None

            def save() -> None:
                if is_edit:
                    assert task is not None
                    assert task.id is not None
                    assert status_input is not None
                    saved_task = update_task(
                        task.id,
                        title_input.value or "",
                        description_input.value or "",
                        priority_input.value,
                        status_input.value,
                        due_date_input.value or None,
                    )
                else:
                    saved_task = create_task(
                        title_input.value or "",
                        description_input.value or "",
                        priority_input.value,
                        due_date_input.value or None,
                    )

                if saved_task is None:
                    return

                refresh_tasks()
                if state["page"] == "calendar":
                    render_calendar()
                if (
                    not is_edit
                    and add_another_checkbox is not None
                    and add_another_checkbox.value
                ):
                    title_input.value = ""
                    description_input.value = ""
                    priority_input.value = "medium"
                    due_date_input.value = default_due_iso
                    description_section.value = False
                else:
                    dialog.close()

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

            with ui.row().classes("w-full items-center justify-between pt-2"):
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
                    with ui.column().classes("flex-1 min-w-0 gap-0"):
                        title_classes = "font-medium text-slate-900 truncate w-full"
                        if is_done:
                            title_classes += " line-through text-slate-400"
                        ui.label(task.title).classes(title_classes)
                        if task.description:
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
                            "text-xs font-semibold text-slate-500 bg-slate-100 rounded-full px-2 py-0.5"
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

                            with ui.row().classes("items-center gap-2"):
                                ui.badge(
                                    task.priority.value.title(),
                                    color=get_priority_color(task.priority.value),
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
        state["selected_date"] = d
        if d.year != state["view_month"].year or d.month != state["view_month"].month:
            state["view_month"] = d.replace(day=1)
        render_calendar()

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

            priority_pill_classes = {
                "low": "bg-emerald-100 text-emerald-700",
                "medium": "bg-amber-100 text-amber-700",
                "high": "bg-rose-100 text-rose-700",
            }

            with ui.row().classes("w-full items-center justify-between gap-4"):
                with ui.column().classes("gap-1"):
                    ui.label("Calendar").classes(
                        "text-2xl font-semibold text-slate-900"
                    )
                    ui.label(view_month.strftime("%B %Y")).classes(
                        "text-sm text-slate-500"
                    )
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

            with ui.row().classes("w-full items-stretch gap-4 flex-nowrap"):
                with ui.card().classes(
                    "flex-1 min-w-0 rounded-2xl shadow-sm !p-0 overflow-hidden"
                ):
                    with ui.element("div").classes(
                        "w-full grid grid-cols-7 bg-slate-50"
                    ):
                        for day_label in ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]:
                            with ui.element("div").classes("py-2 text-center"):
                                ui.label(day_label).classes(
                                    "text-xs font-semibold uppercase text-slate-500"
                                )

                    cal = cal_module.Calendar(firstweekday=0)
                    month_dates = list(
                        cal.itermonthdates(view_month.year, view_month.month)
                    )

                    with ui.element("div").classes(
                        "w-full grid grid-cols-[repeat(7,minmax(0,1fr))] "
                        "border-r border-b border-slate-100"
                    ):
                        for d in month_dates:
                            is_current_month = d.month == view_month.month
                            is_today_cell = d == today
                            is_selected = d == selected

                            cell_classes = (
                                "min-h-[110px] min-w-0 max-w-full overflow-hidden "
                                "border-t border-l border-slate-100 "
                                "p-2 flex flex-col gap-1 cursor-pointer "
                                "hover:bg-slate-50 transition-colors"
                            )
                            if not is_current_month:
                                cell_classes += " bg-slate-50"
                            if is_selected:
                                cell_classes += (
                                    " ring-2 ring-inset ring-teal-500 bg-teal-50/40"
                                )

                            cell = ui.element("div").classes(cell_classes)
                            cell.on("click", lambda day=d: select_date(day))
                            with cell:
                                with ui.element("div").classes(
                                    "w-full flex items-center justify-start pl-3"
                                ):
                                    if is_today_cell:
                                        with ui.element("div").classes(
                                            "w-6 h-6 rounded-full bg-teal-600 "
                                            "flex items-center justify-center"
                                        ):
                                            ui.label(str(d.day)).classes(
                                                "text-xs font-semibold text-white"
                                            )
                                    else:
                                        day_num_classes = "text-xs font-medium "
                                        if not is_current_month:
                                            day_num_classes += "text-slate-400"
                                        else:
                                            day_num_classes += "text-slate-700"
                                        ui.label(str(d.day)).classes(day_num_classes)

                                cell_tasks = tasks_by_date.get(d, [])
                                for t in cell_tasks[:3]:
                                    pill_color = priority_pill_classes.get(
                                        t.priority.value, "bg-slate-100 text-slate-700"
                                    )
                                    text_classes = "text-xs truncate"
                                    if t.completed:
                                        text_classes += " line-through opacity-60"

                                    pill = ui.element("div").classes(
                                        f"w-full max-w-full overflow-hidden "
                                        f"rounded px-1.5 py-0.5 "
                                        f"cursor-pointer {pill_color}"
                                    )
                                    with pill:
                                        ui.label(t.title).classes(
                                            f"block truncate {text_classes}"
                                        )
                                    pill.on(
                                        "click.stop",
                                        lambda task=t: open_task_dialog(task),
                                    )

                                if len(cell_tasks) > 3:
                                    ui.label(f"+{len(cell_tasks) - 3} more").classes(
                                        "text-xs text-slate-500"
                                    )

                with ui.card().classes(
                    "w-80 shrink-0 rounded-2xl shadow-sm !p-0 overflow-hidden"
                ):
                    with ui.column().classes("w-full p-4 gap-3"):
                        with ui.row().classes(
                            "w-full items-start justify-between gap-2"
                        ):
                            with ui.column().classes("gap-0 min-w-0"):
                                ui.label(selected.strftime("%A")).classes(
                                    "text-xs uppercase tracking-widest text-slate-500"
                                )
                                ui.label(selected.strftime("%B %d, %Y")).classes(
                                    "text-lg font-semibold text-slate-900"
                                )
                            add_day_btn = ui.button(icon="add").props(
                                "round dense unelevated color=teal-7"
                            )
                            add_day_btn.tooltip("Add task to this day")
                            add_day_btn.on(
                                "click",
                                lambda: open_task_dialog(
                                    default_due_date=state["selected_date"]
                                ),
                            )

                        selected_tasks = tasks_by_date.get(selected, [])

                        if not selected_tasks:
                            with ui.column().classes(
                                "w-full items-center gap-2 py-8"
                            ):
                                ui.icon("event_available", size="2rem").classes(
                                    "text-slate-300"
                                )
                                ui.label("No tasks for this day").classes(
                                    "text-sm text-slate-500"
                                )
                        else:
                            ui.label(
                                f"{len(selected_tasks)} "
                                f"task{'s' if len(selected_tasks) != 1 else ''}"
                            ).classes("text-xs text-slate-500")

                            for t in selected_tasks:
                                pill_color = priority_pill_classes.get(
                                    t.priority.value,
                                    "bg-slate-100 text-slate-700",
                                )
                                title_classes = "text-sm font-medium text-slate-900"
                                if t.completed:
                                    title_classes += " line-through opacity-60"

                                item = ui.element("div").classes(
                                    "w-full rounded-lg border border-slate-100 "
                                    "p-3 cursor-pointer hover:bg-slate-50 "
                                    "transition-colors"
                                )
                                with item:
                                    ui.label(t.title).classes(title_classes)
                                    with ui.row().classes(
                                        "items-center gap-2 mt-1"
                                    ):
                                        ui.label(t.priority.value.title()).classes(
                                            f"text-xs rounded px-1.5 py-0.5 "
                                            f"{pill_color}"
                                        )
                                        ui.label(t.status.value.replace("_", " ").title()).classes(
                                            "text-xs text-slate-500"
                                        )
                                item.on(
                                    "click",
                                    lambda task=t: open_task_dialog(task),
                                )

    def refresh_tasks() -> None:
        tasks_container.clear()

        all_tasks = get_tasks()
        open_count = sum(1 for t in all_tasks if not t.completed)
        completed_count = sum(1 for t in all_tasks if t.completed)

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
    sort_select.on_value_change(
        lambda e: (state.__setitem__("sort", e.value), refresh_tasks())
    )
    global_search_input.on_value_change(
        lambda e: (state.__setitem__("search", normalize_query(e.value)), refresh_tasks())
    )
    view_toggle.on_value_change(
        lambda e: (state.__setitem__("view", e.value), refresh_tasks())
    )

    render_workspace_nav()
    refresh_tasks()
