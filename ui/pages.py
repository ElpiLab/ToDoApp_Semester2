from datetime import date

from nicegui import ui

from ui.controllers import (
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
    if status == "pending":
        return "warning"
    return "secondary"


def format_due_date(due_date: date | None) -> str:
    return due_date.isoformat() if due_date else "No due date"


def normalize_query(value: str | None) -> str:
    return (value or "").strip().lower()


@ui.page("/")
def index_page():
    ui.query("body").classes("bg-slate-100")
    ui.query(".q-layout").props('view="LHh LpR fFf"')

    state = {"filter": "all", "search": ""}

    with ui.left_drawer(
        value=True, top_corner=True, bottom_corner=True
    ).classes("bg-slate-900 text-white").props("width=260"):
        with ui.column().classes("w-full h-full p-4 gap-0"):
            with ui.row().classes("items-center gap-2 px-2 py-2"):
                ui.icon("bolt").classes("text-2xl text-teal-400")
                ui.label("Bizzy").classes("text-2xl font-bold tracking-wide")
            ui.separator().classes("bg-slate-700 -mx-4")

            ui.label("WORKSPACE").classes(
                "text-xs uppercase tracking-widest text-slate-500 px-3 mt-5 mb-2"
            )
            with ui.column().classes("w-full gap-1"):
                workspace_items = [
                    ("Dashboard", "dashboard", False),
                    ("Tasks", "task_alt", True),
                    ("Calendar", "calendar_month", False),
                    ("Modules", "library_books", False),
                    ("Analytics", "analytics", False),
                ]
                for label, icon, active in workspace_items:
                    item_classes = "w-full justify-start px-3 py-2 rounded-lg"
                    if active:
                        ui.button(label, icon=icon).props(
                            "flat no-caps color=white"
                        ).classes(f"{item_classes} bg-teal-600")
                    else:
                        ui.button(label, icon=icon).props(
                            "flat no-caps color=grey-4"
                        ).classes(item_classes)

            ui.label("SYSTEM").classes(
                "text-xs uppercase tracking-widest text-slate-500 px-3 mt-6 mb-2"
            )
            with ui.column().classes("w-full gap-1"):
                ui.button("Settings", icon="settings").props(
                    "flat no-caps color=grey-4"
                ).classes("w-full justify-start px-3 py-2 rounded-lg")

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
        ui.input(placeholder="Search assignments, courses...").props(
            "outlined dense"
        ).classes("w-80")
        create_button = ui.button("New Task", icon="add").props(
            "color=teal-7 unelevated"
        )
        create_button.classes("rounded-lg px-4")
        ui.button(icon="notifications").props("flat round color=grey-7")
        ui.button(icon="settings").props("flat round color=grey-7")

    with ui.column().classes("w-full gap-6 p-6").style("max-width: 1280px; margin: 0 auto;"):
        with ui.column().classes("gap-1"):
            ui.label("Task List View").classes("text-2xl font-semibold text-slate-900")
            ui.label("Manage coursework, deadlines, and study tasks in one place.").classes(
                "text-sm text-slate-500"
            )

        with ui.row().classes("w-full items-stretch gap-4"):
            summary_value_labels: list = []
            summary_cards = (
                ("Total tasks", "Track your full workload"),
                ("Open tasks", "Focus on what still needs action"),
                ("Completed", "Measure finished work"),
            )
            for title, subtitle in summary_cards:
                with ui.card().classes("col flex-1 min-w-[220px] rounded-2xl shadow-sm"):
                    ui.label(title).classes("text-sm uppercase tracking-wide text-slate-500")
                    summary_value_labels.append(
                        ui.label("0").classes("text-3xl font-semibold text-slate-900")
                    )
                    ui.label(subtitle).classes("text-sm text-slate-500")

        with ui.card().classes("w-full rounded-2xl shadow-sm"):
            with ui.row().classes("w-full items-center justify-between gap-4 p-6"):
                with ui.column().classes("gap-1"):
                    ui.label("Tasks").classes("text-xl font-semibold text-slate-900")
                    ui.label("Filter, search, and manage your study tasks.").classes(
                        "text-sm text-slate-500"
                    )

                with ui.row().classes("items-center gap-3"):
                    filter_toggle = ui.toggle(
                        {"all": "All", "pending": "Open", "completed": "Completed"},
                        value=state["filter"],
                    ).props("unelevated toggle-color=teal-7")
                    search_input = ui.input(
                        placeholder="Search tasks by title...",
                    ).props("clearable outlined")
                    search_input.classes("w-72")

            ui.separator()

            task_list_container = ui.column().classes("w-full gap-0")

    def open_task_dialog(task=None) -> None:
        is_edit = task is not None
        button_label = "Save changes" if is_edit else "Save task"

        with ui.dialog() as dialog, ui.card().classes(
            "w-[540px] max-w-full rounded-2xl p-6 gap-4"
        ):
            ui.label("EDIT TASK" if is_edit else "NEW TASK").classes(
                "text-xs uppercase tracking-widest text-slate-400"
            )
            title_input = (
                ui.input(
                    placeholder="What needs to be done?",
                    value=task.title if is_edit else "",
                )
                .props('borderless input-class="text-2xl"')
                .classes("w-full border-l-4 border-blue-500 pl-3")
            )

            ui.separator()

            with ui.row().classes("w-full items-center gap-4"):
                priority_input = ui.toggle(
                    {"low": "LOW", "medium": "MED", "high": "HIGH"},
                    value=task.priority.value if is_edit else "medium",
                ).props("unelevated toggle-color=orange-7")
                due_date_input = (
                    ui.input(
                        "Due date",
                        value=task.due_date.isoformat() if is_edit and task.due_date else "",
                    )
                    .props("outlined type=date")
                    .classes("w-44")
                )

            status_input = None
            if is_edit:
                status_input = (
                    ui.select(
                        {
                            "created": "Created",
                            "pending": "Pending",
                            "in_progress": "In Progress",
                            "done": "Done",
                        },
                        value=task.status.value,
                        label="Status",
                    )
                    .props("outlined")
                    .classes("w-full")
                )

            description_section = ui.expansion(
                "Add description (optional)",
                icon="add",
                value=is_edit and bool(task.description),
            ).classes("w-full")
            with description_section:
                description_input = (
                    ui.textarea(value=task.description if is_edit else "")
                    .props("outlined autogrow")
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
                if (
                    not is_edit
                    and add_another_checkbox is not None
                    and add_another_checkbox.value
                ):
                    title_input.value = ""
                    description_input.value = ""
                    priority_input.value = "medium"
                    due_date_input.value = ""
                    description_section.value = False
                else:
                    dialog.close()

            with ui.row().classes("w-full items-center justify-between pt-2"):
                if not is_edit:
                    add_another_checkbox = ui.checkbox("Add another")
                else:
                    ui.element("div")
                with ui.row().classes("gap-2"):
                    ui.button("Cancel", on_click=dialog.close).props("flat color=grey-7")
                    ui.button(button_label, on_click=save).props("color=teal-7 unelevated")

        dialog.open()

    def refresh_tasks() -> None:
        task_list_container.clear()

        all_tasks = get_tasks()
        all_tasks.sort(key=lambda task: task.due_date or date.max)

        open_tasks = [task for task in all_tasks if not task.completed]
        completed_tasks = [task for task in all_tasks if task.completed]

        summary_numbers = [len(all_tasks), len(open_tasks), len(completed_tasks)]
        for label, count in zip(summary_value_labels, summary_numbers):
            label.set_text(str(count))

        visible_tasks = all_tasks
        if state["filter"] == "pending":
            visible_tasks = open_tasks
        elif state["filter"] == "completed":
            visible_tasks = completed_tasks

        query = state["search"]
        if query:
            visible_tasks = [task for task in visible_tasks if query in task.title.lower()]

        with task_list_container:
            with ui.row().classes(
                "w-full items-center gap-4 px-6 py-4 text-xs font-semibold uppercase tracking-wide text-slate-500"
            ):
                ui.label("Task").classes("w-64")
                ui.label("Priority").classes("w-24")
                ui.label("Status").classes("w-28")
                ui.label("Due date").classes("w-32")
                ui.label("Actions").classes("grow")

            ui.separator()

            if not visible_tasks:
                with ui.column().classes("w-full items-center gap-3 px-6 py-12 text-center"):
                    ui.icon("inbox", size="3rem").classes("text-slate-300")
                    ui.label("No matching tasks").classes("text-lg font-medium text-slate-700")
                    ui.label(
                        "Create a new task or adjust your filters to see more results."
                    ).classes("text-sm text-slate-500")
                return

            def handle_reopen(task_id: int) -> None:
                if mark_task_pending(task_id):
                    refresh_tasks()

            def handle_complete(task_id: int) -> None:
                if complete_task(task_id):
                    refresh_tasks()

            def handle_delete(task_id: int) -> None:
                if delete_task(task_id):
                    refresh_tasks()

            for task in visible_tasks:
                assert task.id is not None
                with ui.column().classes("w-full gap-0"):
                    with ui.row().classes("w-full items-center gap-4 px-6 py-4"):
                        with ui.column().classes("w-64 gap-1"):
                            ui.label(task.title).classes("font-medium text-slate-900")
                            ui.label(task.description or "No description").classes(
                                "text-sm text-slate-500"
                            )

                        ui.badge(
                            task.priority.value.title(),
                            color=get_priority_color(task.priority.value),
                        )
                        ui.badge(
                            task.status.value.replace("_", " ").title(),
                            color=get_status_color(task.status.value),
                        )
                        ui.label(format_due_date(task.due_date)).classes(
                            "w-32 text-sm text-slate-600"
                        )

                        with ui.row().classes("grow justify-end gap-2"):
                            if task.completed:
                                ui.button(
                                    "Reopen",
                                    icon="undo",
                                    on_click=lambda task_id=task.id: handle_reopen(task_id),
                                ).props("flat color=grey-8")
                            else:
                                ui.button(
                                    "Complete",
                                    icon="check_circle",
                                    on_click=lambda task_id=task.id: handle_complete(task_id),
                                ).props("flat color=positive")

                            ui.button(
                                "Edit",
                                icon="edit",
                                on_click=lambda current_task=task: open_task_dialog(current_task),
                            ).props("flat color=primary")
                            ui.button(
                                "Delete",
                                icon="delete",
                                on_click=lambda task_id=task.id: handle_delete(task_id),
                            ).props("flat color=negative")

                    ui.separator()

    create_button.on("click", lambda: open_task_dialog())
    filter_toggle.on_value_change(lambda e: (state.__setitem__("filter", e.value), refresh_tasks()))
    search_input.on_value_change(
        lambda e: (state.__setitem__("search", normalize_query(e.value)), refresh_tasks())
    )

    refresh_tasks()
