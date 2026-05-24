# 500 Clean Root and Persistence Contract

## Scope

Clean up root-level deployment and persistence drift while tightening task data access APIs.

## Expected Files or Modules to Touch

- `application.py`
- `.vscode/settings.json`
- `src/student_task_manager/data_access/db.py`
- `src/student_task_manager/data_access/dao.py`
- `src/student_task_manager/services/task_service.py`
- `src/student_task_manager/ui/routes.py`
- `src/student_task_manager/ui/login.py`
- `src/student_task_manager/ui/registration.py`
- `src/student_task_manager/ui/tasks_page.py`
- relevant tests under `tests/`
- `README.md`, `docs/Status.md`, `docs/Changelog.md`

## Tests to Add or Update

- Update database config expectations for `sqlite:///data/todo.db`.
- Update DAO/service tests after removing unscoped access methods and `TaskService.filter_tasks()`.
- Keep route registration import behavior covered by existing app tests where possible.

## Acceptance Criteria

- Root `todo.db` is moved to `data/todo.db` when no app process is holding it.
- Local default database URL is `sqlite:///data/todo.db`.
- Unscoped `TaskDAO.get_all()` and `TaskDAO.get_by_id()` are removed.
- `TaskService.filter_tasks()` and its test-only coverage are removed.
- NiceGUI route registration is explicit rather than relying on named unused imports in `application.py`.
- Unused callback event args are cleaned where practical.
- `.vscode/settings.json` no longer tells VS Code to prefer Conda.
- Relevant docs reflect the new local database location and cleanup.

## Archive Condition

Archive after implementation and verification with the repository's required checks, or document any unavailable check explicitly.
