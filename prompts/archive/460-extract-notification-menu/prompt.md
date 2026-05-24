# 460 Extract Notification Menu

## Scope

Extract notification menu rendering and read-state helpers from `src/student_task_manager/ui/pages.py` into `src/student_task_manager/ui/notifications.py`.

Keep route setup, app shell layout, sidebar navigation, page state, task refresh orchestration, and service callbacks in `pages.py`.

## Expected Files

- `src/student_task_manager/ui/pages.py`
- `src/student_task_manager/ui/notifications.py`
- `docs/Changelog.md`
- `docs/Roadmap.md`
- `docs/Status.md`

## Tests

- Run focused UI page tests first.
- Run mypy and ruff checks for touched modules.
- Run full gates after extraction and manual smoke testing.

## Acceptance Criteria

- Notification bell dot still reflects unread overdue/upcoming notifications.
- Notification menu still lists overdue and upcoming tasks.
- Clicking a notification still opens the task dialog and marks it read.
- Mark all read still persists session read state.
- `pages.py` keeps ownership of app shell state and refresh orchestration.
- No behavior change is intended.

## Archive Condition

Archive this prompt after implementation, verification, and manual smoke testing.
