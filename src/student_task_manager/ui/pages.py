from datetime import date

from nicegui import app, ui
from student_task_manager.ui.analytics_page import render_analytics_page
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

    ui.colors(primary="#15803d")
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
        ".notif-dot.q-badge--floating "
        "{ top: 8px !important; right: 8px !important; min-width: 8px !important; "
        "width: 8px !important; height: 8px !important; padding: 0 !important; }"
        ".task-view-toggle .q-btn "
        "{ min-height: 40px; padding: 0 16px; border-radius: 0 !important; }"
        ".task-view-toggle .q-btn + .q-btn { border-left: 1px solid #e2e8f0; }"
        ".task-view-toggle .q-btn:not(.q-btn--active) "
        "{ background: #ffffff !important; color: #475569 !important; }"
        ".task-view-toggle .q-btn:not(.q-btn--active):not([aria-pressed='true']) "
        "{ background: #ffffff !important; color: #475569 !important; }"
        ".task-view-toggle .q-btn:not(.q-btn--active):not([aria-pressed='true']):hover "
        "{ background: #f0fdf4 !important; color: #15803d !important; }"
        ".task-view-toggle .q-btn.q-btn--active, "
        ".task-view-toggle .q-btn[aria-pressed='true'] "
        "{ background: #dcfce7 !important; color: #15803d !important; font-weight: 600; }"
        "</style>"
    )

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

    drawer_state = {"open": True}
    drawer = (
        ui.left_drawer(value=True, top_corner=False, bottom_corner=True)
        .classes("bg-white text-slate-900 border-r border-slate-200")
        .props("width=260")
    )

    def toggle_sidebar() -> None:
        drawer_state["open"] = not drawer_state["open"]
        drawer.set_value(drawer_state["open"])
        expand_btn.set_visibility(not drawer_state["open"])

    with drawer:
        with ui.column().classes("w-full h-full pt-4 px-4 pb-4 gap-0"):
            with ui.row().classes("w-full items-center pl-3 mb-2"):
                ui.label("WORKSPACE").classes(
                    "text-xs uppercase tracking-widest text-slate-400 flex-1 sidebar-hide"
                )
                collapse_btn = ui.button(icon="chevron_left").props("flat round dense color=grey-7")
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
                                .props("flat no-caps align=left color=green-9")
                                .classes(f"{item_classes} bg-emerald-50 font-semibold")
                            )
                        else:
                            btn = (
                                ui.button(label, icon=icon)
                                .props("flat no-caps align=left color=grey-8")
                                .classes(item_classes)
                            )
                        if key in ("dashboard", "tasks", "calendar", "analytics"):
                            btn.on("click", lambda k=key: switch_to_page(k))
                        nav_buttons[key] = btn

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
                render_workspace_nav()

            ui.element("div").classes("flex-1")
            with ui.element("div").classes("w-full border-t border-slate-200 pt-3 mt-4"):
                with (
                    ui.button()
                    .props("flat no-caps align=left color=grey-8")
                    .classes("w-full rounded-lg p-2")
                ):
                    with ui.row().classes("w-full items-center gap-3 no-wrap"):
                        with ui.element("div").classes(
                            "w-9 h-9 rounded-full bg-emerald-600 "
                            "flex items-center justify-center shrink-0"
                        ):
                            avatar_label = ui.label(avatar_initial).classes(
                                "text-white font-semibold text-sm"
                            )
                        with ui.column().classes("gap-0 min-w-0 sidebar-hide"):
                            sidebar_name_label = ui.label(display_name).classes(
                                "text-sm font-medium text-slate-900 truncate max-w-[160px]"
                            )
                    user_menu = ui.menu().props('anchor="top left" self="bottom left"')
                    with user_menu:
                        with ui.column().classes("p-3 gap-1 min-w-[220px]"):
                            with ui.column().classes("gap-0 pb-2 mb-1 border-b border-slate-200"):
                                menu_name_label = ui.label(display_name).classes(
                                    "text-sm font-medium text-slate-900"
                                )
                                menu_email_label = ui.label(display_email).classes(
                                    "text-xs text-slate-500"
                                )
                            settings_menu_btn = ui.button("Settings", icon="settings").props(
                                "flat no-caps align=left color=grey-8"
                            )
                            settings_menu_btn.classes("w-full justify-start px-2 py-1 rounded-md")
                            settings_menu_btn.on(
                                "click",
                                lambda: (
                                    user_menu.close(),
                                    switch_to_page("settings"),
                                ),
                            )
                            logout_menu_btn = ui.button("Logout", icon="logout").props(
                                "flat no-caps align=left color=grey-8"
                            )
                            logout_menu_btn.classes("w-full justify-start px-2 py-1 rounded-md")
                            logout_menu_btn.on(
                                "click",
                                lambda: ui.navigate.to("/logout"),
                            )

    def refresh_user_badge() -> None:
        new_name = app.storage.user.get("full_name") or app.storage.user.get("email") or "User"
        new_email = app.storage.user.get("email") or ""
        new_initial = (new_name[0] if new_name else "?").upper()
        avatar_label.set_text(new_initial)
        sidebar_name_label.set_text(new_name)
        menu_name_label.set_text(new_name)
        menu_email_label.set_text(new_email)

    expand_btn = (
        ui.button(icon="chevron_right")
        .props("flat round dense color=grey-7")
        .classes("fixed top-20 left-2 z-50 bg-white shadow-md rounded-full")
    )
    expand_btn.tooltip("Open sidebar")
    expand_btn.set_visibility(False)
    expand_btn.on("click", toggle_sidebar)

    with (
        ui.header()
        .classes("bg-white items-center px-6 py-3 border-b border-slate-200")
        .props("flat")
    ):
        with ui.row().classes("items-center flex-1"):
            with ui.row().classes("items-center gap-2"):
                ui.html('<img src="/assets/logo.svg" alt="Bizzy" class="h-11 w-auto" />')

        with ui.row().classes("items-center gap-3 flex-1 justify-end"):
            create_button = ui.button("New task", icon="add").props(
                'color=green-9 unelevated no-caps dense padding="6px 10px"'
            )
            create_button.classes("rounded-lg new-task-btn")
            with ui.row().classes("items-center gap-1"):
                with ui.button(icon="notifications").props("flat round color=grey-7"):
                    notif_badge = (
                        ui.badge("", color="red")
                        .props("floating rounded")
                        .classes("notif-dot !w-2 !h-2 !min-h-0 !p-0")
                    )
                    notif_badge.set_visibility(False)
                    notif_menu = ui.menu().props(
                        'anchor="bottom right" self="top right" :offset="[0, 12]"'
                    )
                    with notif_menu:
                        notif_menu_container = ui.column().classes(
                            "p-0 gap-0 w-80 max-h-[420px] overflow-y-auto"
                        )
                settings_header_btn = ui.button(icon="settings").props("flat round color=grey-7")
                settings_header_btn.tooltip("Settings")
                settings_header_btn.on("click", lambda: switch_to_page("settings"))

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
            refresh_user_badge,
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

    create_button.on("click", lambda: open_task_dialog())
    render_workspace_nav()
    refresh_tasks()
    render_dashboard()
