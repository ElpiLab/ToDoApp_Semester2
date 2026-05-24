from datetime import date

from nicegui import app, ui
from student_task_manager.ui.analytics_page import render_analytics_page
from student_task_manager.ui.app_shell import AppShell
from student_task_manager.ui.calendar_page import render_calendar_page
from student_task_manager.ui.controllers import (
    change_task_status,
    complete_task,
    delete_task,
    get_tasks,
    mark_task_pending,
)
from student_task_manager.ui.dashboard_page import render_dashboard_page
from student_task_manager.ui.notifications import NotificationMenu
from student_task_manager.ui.settings_page import render_settings_page
from student_task_manager.ui.task_dialog import open_task_dialog as open_task_dialog_modal
from student_task_manager.ui.tasks_page import (
    render_board,
    render_empty_state,
    render_list,
    render_task_controls,
)
from student_task_manager.ui.view_helpers import task_matches_status_filter


@ui.page("/logout")
def logout_page():
    app.storage.user.clear()
    ui.navigate.to("/login")


@ui.page("/")
def index_page():
    if not app.storage.user.get("authenticated", False):
        ui.navigate.to("/login")
        return

    state = {
        "status": "all",
        "priority": "all",
        "category": "all",
        "search": "",
        "view": "board",
        "dragging": None,
        "page": "dashboard",
        "view_month": date.today().replace(day=1),
        "selected_date": date.today(),
        "calendar_filter_date": None,
    }

    display_name = app.storage.user.get("full_name") or app.storage.user.get("email") or "User"
    avatar_initial = (display_name[0] if display_name else "?").upper()
    display_email = app.storage.user.get("email") or ""
    read_notification_keys: set[str] = set(app.storage.user.get("read_notif_keys") or [])

    shell: AppShell | None = None

    def switch_to_page(page_key: str) -> None:
        state["page"] = page_key
        dashboard_panel.set_visibility(page_key == "dashboard")
        tasks_panel.set_visibility(page_key == "tasks")
        calendar_panel.set_visibility(page_key == "calendar")
        analytics_panel.set_visibility(page_key == "analytics")
        settings_panel.set_visibility(page_key == "settings")
        if page_key == "dashboard":
            render_dashboard()
        if page_key == "calendar":
            render_calendar()
        if page_key == "analytics":
            render_analytics()
        if page_key == "settings":
            render_settings()
        if shell is not None:
            shell.render_workspace_nav()

    shell = AppShell(
        state=state,
        display_name=display_name,
        display_email=display_email,
        avatar_initial=avatar_initial,
        on_page_selected=switch_to_page,
        on_new_task=lambda: open_task_dialog(),
    )
    notif_badge, notif_menu_container = shell.render()

    with ui.column().classes("w-full gap-4 p-6 mx-auto").style("max-width: 1280px;"):
        dashboard_panel = ui.column().classes("w-full gap-6")

        tasks_panel = ui.column().classes("w-full gap-4")
        tasks_panel.set_visibility(False)
        with tasks_panel:
            task_controls = render_task_controls(
                view=state["view"],
                status=state["status"],
                priority=state["priority"],
                category=state["category"],
                on_status_change=lambda value: (
                    state.__setitem__("status", value),
                    refresh_tasks(),
                ),
                on_priority_change=lambda value: (
                    state.__setitem__("priority", value),
                    refresh_tasks(),
                ),
                on_category_change=lambda value: (
                    state.__setitem__("category", value),
                    refresh_tasks(),
                ),
                on_search_change=lambda value: (
                    state.__setitem__("search", value),
                    refresh_tasks(),
                ),
                on_view_change=lambda value: (
                    state.__setitem__("view", value),
                    refresh_tasks(),
                ),
            )

            tasks_container = ui.column().classes("w-full")

        calendar_panel = ui.column().classes("w-full gap-4")
        calendar_panel.set_visibility(False)

        analytics_panel = ui.column().classes("w-full gap-6")
        analytics_panel.set_visibility(False)

        settings_panel = ui.column().classes("w-full max-w-xl gap-6")
        settings_panel.set_visibility(False)

    def open_task_dialog(task=None, default_due_date: date | None = None) -> None:
        open_task_dialog_modal(
            task,
            default_due_date,
            current_page=lambda: state["page"],
            refresh_tasks=refresh_tasks,
            render_calendar=render_calendar,
            render_dashboard=render_dashboard,
            render_analytics=render_analytics,
        )

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
        render_dashboard_page(
            dashboard_panel,
            get_tasks,
            display_name,
            complete_task,
            refresh_tasks,
            open_task_dialog,
            switch_to_page,
        )

    def render_analytics() -> None:
        render_analytics_page(analytics_panel, get_tasks)

    def render_settings() -> None:
        render_settings_page(
            settings_panel,
            get_tasks,
            delete_task,
            refresh_tasks,
            shell.refresh_user_badge,
        )

    def render_calendar() -> None:
        render_calendar_page(
            calendar_panel,
            get_tasks,
            state["view_month"],
            state["selected_date"],
            state["calendar_filter_date"],
            navigate_to_today,
            navigate_month,
            select_date,
            clear_calendar_filter,
            open_task_dialog,
        )

    notification_menu = NotificationMenu(
        badge=notif_badge,
        container=notif_menu_container,
        read_keys=read_notification_keys,
        get_tasks=get_tasks,
        open_task_dialog=lambda task: open_task_dialog(task),
        persist_read_keys=lambda keys: app.storage.user.update({"read_notif_keys": list(keys)}),
    )

    def refresh_tasks() -> None:
        tasks_container.clear()

        all_tasks = get_tasks()
        active_count = sum(1 for t in all_tasks if not t.completed)
        completed_count = sum(1 for t in all_tasks if t.completed)

        notification_menu.render()

        task_controls.subtitle_label.set_text(f"{active_count} active · {completed_count} done")

        visible_tasks = list(all_tasks)
        visible_tasks = [t for t in visible_tasks if task_matches_status_filter(t, state["status"])]
        if state["priority"] != "all":
            visible_tasks = [t for t in visible_tasks if t.priority.value == state["priority"]]
        if state["category"] != "all":
            visible_tasks = [t for t in visible_tasks if t.category == state["category"]]

        query = state["search"]
        if query:
            visible_tasks = [t for t in visible_tasks if query in t.title.lower()]

        def handle_reopen(task_id: int) -> None:
            if mark_task_pending(task_id):
                refresh_tasks()

        def handle_complete(task_id: int) -> None:
            if complete_task(task_id):
                refresh_tasks()

        def handle_delete(task_id: int) -> None:
            if delete_task(task_id):
                refresh_tasks()

        def handle_status_change(task_id: int, status: str) -> None:
            change_task_status(task_id, status)
            refresh_tasks()

        def handle_drag_start(task_id: int) -> None:
            state["dragging"] = task_id

        def handle_drop_status(target_status: str) -> None:
            dragging_id = state.get("dragging")
            if dragging_id is None:
                return
            state["dragging"] = None
            if change_task_status(dragging_id, target_status) is not None:
                refresh_tasks()

        with tasks_container:
            if not all_tasks:
                with ui.column().classes("w-full items-center gap-3 py-16"):
                    ui.icon("celebration", size="3rem").classes("text-emerald-500")
                    ui.label("Welcome to Bizzy").classes("text-xl font-semibold text-slate-900")
                    ui.label("Create your first task to get started.").classes(
                        "text-sm text-slate-500"
                    )
                    welcome_btn = ui.button("New task", icon="add").props(
                        "color=green-9 unelevated no-caps"
                    )
                    welcome_btn.on("click", lambda: open_task_dialog())
                return

            if not visible_tasks:
                render_empty_state()
                return

            if state["view"] == "board":
                render_board(
                    visible_tasks,
                    on_edit=open_task_dialog,
                    on_add_task=open_task_dialog,
                    on_drag_start=handle_drag_start,
                    on_drop_status=handle_drop_status,
                )
            else:
                with ui.column().classes("w-full gap-0"):
                    render_list(
                        visible_tasks,
                        on_complete=handle_complete,
                        on_reopen=handle_reopen,
                        on_delete=handle_delete,
                        on_edit=open_task_dialog,
                        on_status_change=handle_status_change,
                    )

    shell.render_workspace_nav()
    refresh_tasks()
    render_dashboard()
