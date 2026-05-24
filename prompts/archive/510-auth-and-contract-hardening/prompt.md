# 510 Auth and Contract Hardening

## Scope

Harden authentication, startup seeding, scoped deletion, and repository contract docs after the root/persistence cleanup.

## Expected Files or Modules to Touch

- `application.py`
- `src/student_task_manager/domain/models.py`
- `src/student_task_manager/services/auth_service.py`
- `src/student_task_manager/services/task_service.py`
- `src/student_task_manager/data_access/dao.py`
- `src/student_task_manager/ui/registration.py`
- `src/student_task_manager/ui/settings_page.py`
- relevant tests under `tests/`
- `AGENTS.md`, `README.md`, `docs/TestCases.md`, `docs/Status.md`, `docs/Changelog.md`, `docs/Roadmap.md`
- `.vscode/settings.json`

## Tests to Add or Update

- Cover dev-admin startup gating and required password configuration.
- Cover `AuthService.register(...)` validation and duplicate-email behavior.
- Cover `AuthService.update_profile(...)` raising `ValueError("User not found")`.
- Update DAO/service delete tests for `delete_for_user(task_id, user_id)`.
- Sync test-case documentation with the actual automated tests.

## Acceptance Criteria

- Default admin creation only runs when an explicit development env flag is enabled and a password env var is present.
- Startup fails with clear exceptions for invalid dev-admin configuration instead of swallowing broad errors.
- Registration persistence and validation live in `AuthService.register(...)`; the UI catches service validation errors.
- `Student.is_active` is removed from the model and docs because inactive users are out of scope.
- DAO deletion is user-scoped through `delete_for_user(task_id, user_id)`.
- `docs/TestCases.md` references real tests.
- `AGENTS.md` project status is no longer stale.
- `.vscode/settings.json` and the empty `.vscode` folder are removed.
- `runtime.txt` is either justified in docs or updated consistently with the Python tooling target.

## Archive Condition

Archive after implementation and verification with the repository's required checks, or document any unavailable check explicitly.
