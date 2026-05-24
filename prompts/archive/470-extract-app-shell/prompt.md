# 470 Extract App Shell

## Scope

Extract shared app shell rendering from `src/student_task_manager/ui/pages.py` into `src/student_task_manager/ui/app_shell.py`.

The app shell includes the sidebar, workspace navigation, header, logo, new-task button, notification button container, settings shortcut, and user profile menu.

Keep page route setup, page state, task refresh orchestration, page renderer callbacks, and task dialog orchestration in `pages.py`.

## Expected Files

- `src/student_task_manager/ui/pages.py`
- `src/student_task_manager/ui/app_shell.py`
- `docs/Changelog.md`
- `docs/Roadmap.md`
- `docs/Status.md`

## Tests

- Run focused UI page tests first.
- Run mypy and ruff checks for touched modules.
- Run full gates after extraction and manual smoke testing when practical.

## Acceptance Criteria

- Sidebar collapse/expand still works.
- Sidebar navigation still switches Dashboard, Tasks, Calendar, Analytics, and Settings.
- Header "New task" still opens the task dialog.
- Header settings button and profile-menu Settings still open Settings.
- Profile menu still displays current user name/email and Logout works.
- Notification bell container is still available to `NotificationMenu`.
- No behavior change is intended.

## Archive Condition

Archive this prompt after implementation, verification, and manual smoke testing.
