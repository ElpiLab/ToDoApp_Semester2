from collections.abc import Callable
from typing import Any

from nicegui import app, ui

from student_task_manager.domain.models import Task
from student_task_manager.domain.validation import is_valid_email
from student_task_manager.services.auth_service import AuthService


def render_settings_page(
    settings_panel: Any,
    get_tasks: Callable[[], list[Task]],
    on_delete_task: Callable[[int], bool],
    on_delete_all_tasks: Callable[[], int],
    on_refresh_tasks: Callable[[], None],
    on_refresh_user_badge: Callable[[], None],
) -> None:
    settings_panel.clear()
    with settings_panel:
        all_tasks = get_tasks()
        total = len(all_tasks)

        with ui.column().classes("gap-1"):
            ui.label("Settings").classes("text-2xl font-semibold text-slate-900")
            ui.label("Account and data").classes("text-sm text-slate-500")

        def section_card(
            title: str,
            subtitle: str,
            icon: str,
            icon_bg: str,
            icon_color: str,
        ):
            card = ui.card().classes("w-full !max-w-lg rounded-2xl shadow-sm !p-6 gap-3")
            with card:
                with ui.row().classes("items-center gap-3"):
                    with ui.element("div").classes(
                        f"w-10 h-10 rounded-xl {icon_bg} flex items-center justify-center shrink-0"
                    ):
                        ui.icon(icon, size="1.25rem").classes(icon_color)
                    ui.label(title).classes("text-xl font-semibold text-slate-900")
                ui.label(subtitle).classes("text-sm text-slate-500 -mt-1")
            return card

        with section_card(
            "Profile",
            "Your account details",
            "person",
            "bg-emerald-100",
            "text-emerald-700",
        ):
            name_input = (
                ui.input(
                    label="Display name",
                    value=app.storage.user.get("full_name") or "",
                )
                .props("outlined dense hide-bottom-space")
                .classes("w-64")
            )
            email_input = (
                ui.input(
                    label="Email",
                    value=app.storage.user.get("email") or "",
                )
                .props("outlined dense hide-bottom-space")
                .classes("w-64")
            )
            profile_password_input = (
                ui.input(
                    label="Current password for email changes",
                    password=True,
                    password_toggle_button=True,
                )
                .props("outlined dense hide-bottom-space")
                .classes("w-64")
            )
            initial_profile = {
                "name": (name_input.value or "").strip(),
                "email": (email_input.value or "").strip(),
            }

            def is_profile_dirty() -> bool:
                return (name_input.value or "").strip() != initial_profile["name"] or (
                    email_input.value or ""
                ).strip() != initial_profile["email"]

            def check_profile_dirty() -> None:
                if is_profile_dirty():
                    save_btn.enable()
                else:
                    save_btn.disable()

            def save_profile() -> None:
                user_id = app.storage.user.get("user_id")
                if not user_id:
                    ui.notify(
                        "Not logged in",
                        type="negative",
                        position="top-right",
                    )
                    return
                new_name = (name_input.value or "").strip()
                new_email = (email_input.value or "").strip()
                if not new_name:
                    ui.notify(
                        "Name cannot be empty",
                        type="negative",
                        position="top-right",
                    )
                    return
                if not is_valid_email(new_email):
                    ui.notify(
                        "Enter a valid email address",
                        type="negative",
                        position="top-right",
                    )
                    return
                try:
                    AuthService().update_profile(
                        user_id,
                        new_name,
                        new_email,
                        current_password=profile_password_input.value or None,
                    )
                except ValueError as e:
                    ui.notify(
                        str(e),
                        type="negative",
                        position="top-right",
                    )
                    return
                app.storage.user.update({"full_name": new_name, "email": new_email})
                profile_password_input.value = ""
                on_refresh_user_badge()
                ui.notify(
                    "Profile saved",
                    type="positive",
                    position="top-right",
                )
                initial_profile.update({"name": new_name, "email": new_email})
                save_btn.disable()

            save_btn = (
                ui.button("Update profile", on_click=save_profile)
                .props('color=green-9 unelevated no-caps padding="10px 24px"')
                .classes("rounded-lg mt-2")
            )
            save_btn.disable()
            name_input.on_value_change(lambda _: check_profile_dirty())
            email_input.on_value_change(lambda _: check_profile_dirty())
            profile_password_input.on_value_change(lambda _: check_profile_dirty())

            ui.separator().classes("mt-3")
            password_expansion = ui.expansion("Change password", icon="lock").classes(
                "w-full text-sm font-semibold text-slate-700"
            )
            password_expansion.props("dense header-class=px-0")

            with password_expansion, ui.column().classes("w-full gap-3 pt-2"):
                current_pw_input = (
                    ui.input(
                        label="Current password",
                        password=True,
                        password_toggle_button=True,
                    )
                    .props("outlined dense hide-bottom-space")
                    .classes("w-64")
                )
                new_pw_input = (
                    ui.input(
                        label="New password",
                        password=True,
                        password_toggle_button=True,
                    )
                    .props("outlined dense hide-bottom-space")
                    .classes("w-64")
                )
                confirm_pw_input = (
                    ui.input(
                        label="Confirm new password",
                        password=True,
                        password_toggle_button=True,
                    )
                    .props("outlined dense hide-bottom-space")
                    .classes("w-64")
                )

            def is_password_dirty() -> bool:
                return bool(
                    (current_pw_input.value or "")
                    or (new_pw_input.value or "")
                    or (confirm_pw_input.value or "")
                )

            def check_password_dirty() -> None:
                if is_password_dirty():
                    password_btn.enable()
                else:
                    password_btn.disable()

            def save_password() -> None:
                user_id = app.storage.user.get("user_id")
                if not user_id:
                    ui.notify("Not logged in", type="negative", position="top-right")
                    return
                current = current_pw_input.value or ""
                new = new_pw_input.value or ""
                confirm = confirm_pw_input.value or ""
                if not current or not new or not confirm:
                    ui.notify("Fill in all password fields", type="negative", position="top-right")
                    return
                if len(new) < 10:
                    ui.notify(
                        "New password must be at least 10 characters",
                        type="negative",
                        position="top-right",
                    )
                    return
                if new != confirm:
                    ui.notify("New passwords do not match", type="negative", position="top-right")
                    return
                if new == current:
                    ui.notify(
                        "New password must differ from the current one",
                        type="negative",
                        position="top-right",
                    )
                    return
                try:
                    AuthService().change_password(user_id, current, new)
                except ValueError as e:
                    ui.notify(str(e), type="negative", position="top-right")
                    return
                current_pw_input.value = ""
                new_pw_input.value = ""
                confirm_pw_input.value = ""
                password_btn.disable()
                ui.notify("Password updated", type="positive", position="top-right")

            with password_expansion:
                password_btn = (
                    ui.button("Update password", on_click=save_password)
                    .props('color=green-9 unelevated no-caps padding="10px 24px"')
                    .classes("rounded-lg mt-2")
                )
                password_btn.disable()
            current_pw_input.on_value_change(lambda _: check_password_dirty())
            new_pw_input.on_value_change(lambda _: check_password_dirty())
            confirm_pw_input.on_value_change(lambda _: check_password_dirty())

        with section_card(
            "Danger zone",
            "Remove your task data",
            "storage",
            "bg-rose-100",
            "text-rose-700",
        ):

            def confirm_delete_all() -> None:
                if not all_tasks:
                    return
                with (
                    ui.dialog().props("persistent") as dialog,
                    ui.card().classes("w-[420px] max-w-full rounded-2xl p-6 gap-3"),
                ):
                    ui.label(f"Permanently delete all {total} tasks?").classes(
                        "text-lg font-semibold text-slate-900"
                    )
                    ui.label(
                        "Every task, including completed ones, "
                        "will be removed. This cannot be undone."
                    ).classes("text-sm text-slate-500")

                    def confirm() -> None:
                        dialog.close()
                        on_delete_all_tasks()
                        on_refresh_tasks()
                        render_settings_page(
                            settings_panel,
                            get_tasks,
                            on_delete_task,
                            on_delete_all_tasks,
                            on_refresh_tasks,
                            on_refresh_user_badge,
                        )

                    with ui.row().classes("w-full justify-end gap-2 pt-2"):
                        ui.button("Cancel", on_click=dialog.close).props(
                            "flat color=grey-7 no-caps"
                        )
                        ui.button("Delete all tasks", on_click=confirm).props(
                            "color=negative unelevated no-caps"
                        )
                dialog.open()

            with ui.column().classes("w-full gap-2"):
                ui.label(
                    "Permanently removes every task in your account. This cannot be undone."
                ).classes("text-xs text-slate-500 leading-relaxed")
                delete_all_btn = (
                    ui.button("Delete all tasks")
                    .props('unelevated no-caps color=negative padding="10px 24px"')
                    .classes("rounded-lg mt-2 self-start")
                )
                delete_all_btn.on("click", confirm_delete_all)
                if not all_tasks:
                    delete_all_btn.props("disable")
                    ui.label("No tasks to delete yet.").classes("text-xs text-slate-400")
