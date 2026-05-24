from collections.abc import Callable
from typing import Any

from nicegui import app, ui


class AppShell:
    """Render the shared application frame around the feature pages.

    Callbacks keep the shell independent from feature renderers and avoid
    circular imports between navigation chrome and page modules.
    """

    def __init__(
        self,
        *,
        state: dict[str, Any],
        display_name: str,
        display_email: str,
        avatar_initial: str,
        on_page_selected: Callable[[str], None],
        on_new_task: Callable[[], None],
    ) -> None:
        self.state = state
        self.display_name = display_name
        self.display_email = display_email
        self.avatar_initial = avatar_initial
        self.on_page_selected = on_page_selected
        self.on_new_task = on_new_task

        self.drawer_state = {"open": True}
        self.drawer: Any | None = None
        self.expand_btn: Any | None = None
        self.workspace_nav_container: Any | None = None
        self.nav_buttons: dict[str, Any] = {}
        self.avatar_label: Any | None = None
        self.sidebar_name_label: Any | None = None
        self.menu_name_label: Any | None = None
        self.menu_email_label: Any | None = None
        self.user_menu: Any | None = None

    def render(self) -> tuple[Any, Any]:
        self._configure_theme()
        self._render_drawer()
        self._render_expand_button()
        return self._render_header()

    def _configure_theme(self) -> None:
        ui.colors(primary="#15803d")
        ui.query("body").classes("bg-stone-100")
        ui.query(".q-layout").props('view="lHh LpR fFf"')
        # Quasar owns several component styles, so shared overrides live beside
        # the shell elements that depend on them.
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

    def _toggle_sidebar(self) -> None:
        self.drawer_state["open"] = not self.drawer_state["open"]
        if self.drawer is not None:
            self.drawer.set_value(self.drawer_state["open"])
        if self.expand_btn is not None:
            self.expand_btn.set_visibility(not self.drawer_state["open"])

    def _render_drawer(self) -> None:
        self.drawer = (
            ui.left_drawer(value=True, top_corner=False, bottom_corner=True)
            .classes("bg-white text-slate-900 border-r border-slate-200")
            .props("width=260")
        )

        with self.drawer:
            with ui.column().classes("w-full h-full pt-4 px-4 pb-4 gap-0"):
                with ui.row().classes("w-full items-center pl-3 mb-2"):
                    ui.label("WORKSPACE").classes(
                        "text-xs uppercase tracking-widest text-slate-400 flex-1 sidebar-hide"
                    )
                    collapse_btn = ui.button(icon="chevron_left").props(
                        "flat round dense color=grey-7"
                    )
                    collapse_btn.tooltip("Collapse sidebar")
                    collapse_btn.on("click", self._toggle_sidebar)

                self.workspace_nav_container = ui.column().classes("w-full gap-2")
                self.render_workspace_nav()

                ui.element("div").classes("flex-1")
                self._render_user_menu()

    def render_workspace_nav(self) -> None:
        if self.workspace_nav_container is None:
            return

        self.workspace_nav_container.clear()
        with self.workspace_nav_container:
            workspace_items = [
                ("Dashboard", "dashboard", "dashboard"),
                ("Tasks", "task_alt", "tasks"),
                ("Calendar", "calendar_month", "calendar"),
                ("Analytics", "analytics", "analytics"),
            ]
            for label, icon, key in workspace_items:
                is_active = self.state["page"] == key
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
                btn.on("click", lambda k=key: self.on_page_selected(k))
                self.nav_buttons[key] = btn

    def _render_user_menu(self) -> None:
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
                        self.avatar_label = ui.label(self.avatar_initial).classes(
                            "text-white font-semibold text-sm"
                        )
                    with ui.column().classes("gap-0 min-w-0 sidebar-hide"):
                        self.sidebar_name_label = ui.label(self.display_name).classes(
                            "text-sm font-medium text-slate-900 truncate max-w-[160px]"
                        )
                self.user_menu = ui.menu().props('anchor="top left" self="bottom left"')
                with self.user_menu:
                    with ui.column().classes("p-3 gap-1 min-w-[220px]"):
                        with ui.column().classes("gap-0 pb-2 mb-1 border-b border-slate-200"):
                            self.menu_name_label = ui.label(self.display_name).classes(
                                "text-sm font-medium text-slate-900"
                            )
                            self.menu_email_label = ui.label(self.display_email).classes(
                                "text-xs text-slate-500"
                            )
                        settings_menu_btn = ui.button("Settings", icon="settings").props(
                            "flat no-caps align=left color=grey-8"
                        )
                        settings_menu_btn.classes("w-full justify-start px-2 py-1 rounded-md")
                        settings_menu_btn.on("click", self._open_settings_from_menu)

                        logout_menu_btn = ui.button("Logout", icon="logout").props(
                            "flat no-caps align=left color=grey-8"
                        )
                        logout_menu_btn.classes("w-full justify-start px-2 py-1 rounded-md")
                        logout_menu_btn.on("click", lambda: ui.navigate.to("/logout"))

    def _open_settings_from_menu(self) -> None:
        if self.user_menu is not None:
            self.user_menu.close()
        self.on_page_selected("settings")

    def refresh_user_badge(self) -> None:
        new_name = app.storage.user.get("full_name") or app.storage.user.get("email") or "User"
        new_email = app.storage.user.get("email") or ""
        new_initial = (new_name[0] if new_name else "?").upper()

        if self.avatar_label is not None:
            self.avatar_label.set_text(new_initial)
        if self.sidebar_name_label is not None:
            self.sidebar_name_label.set_text(new_name)
        if self.menu_name_label is not None:
            self.menu_name_label.set_text(new_name)
        if self.menu_email_label is not None:
            self.menu_email_label.set_text(new_email)

    def _render_expand_button(self) -> None:
        self.expand_btn = (
            ui.button(icon="chevron_right")
            .props("flat round dense color=grey-7")
            .classes("fixed top-20 left-2 z-50 bg-white shadow-md rounded-full")
        )
        self.expand_btn.tooltip("Open sidebar")
        self.expand_btn.set_visibility(False)
        self.expand_btn.on("click", self._toggle_sidebar)

    def _render_header(self) -> tuple[Any, Any]:
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
                create_button.on("click", lambda: self.on_new_task())

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
                    settings_header_btn = ui.button(icon="settings").props(
                        "flat round color=grey-7"
                    )
                    settings_header_btn.tooltip("Settings")
                    settings_header_btn.on("click", lambda: self.on_page_selected("settings"))

        return notif_badge, notif_menu_container
