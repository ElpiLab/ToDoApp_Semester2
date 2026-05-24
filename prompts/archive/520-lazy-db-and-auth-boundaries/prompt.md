# 520 Lazy DB and Auth Boundaries

## Scope

Finish persistence and authentication hardening by removing import-time engine creation, moving auth session ownership out of UI pages, tightening task update transitions, and cleaning current SQLite schema drift.

## Expected Files or Modules to Touch

- `application.py`
- `src/student_task_manager/data_access/db.py`
- `src/student_task_manager/data_access/dao.py`
- `src/student_task_manager/services/auth_service.py`
- `src/student_task_manager/services/task_service.py`
- `src/student_task_manager/ui/login.py`
- `src/student_task_manager/ui/registration.py`
- `src/student_task_manager/ui/settings_page.py`
- relevant tests under `tests/`
- `README.md`, `docs/Status.md`, `docs/Changelog.md`, `docs/Roadmap.md`

## Tests to Add or Update

- Regression tests for `TaskService.update_task(...)` status-only updates on legacy short titles.
- Regression tests for `completed=False` not demoting an in-progress task.
- Auth tests for empty login fields and malformed stored password hashes.
- Startup/deployment tests for missing `STORAGE_SECRET`.
- DB config tests for lazy engine/session behavior.

## Acceptance Criteria

- Physical local SQLite tables no longer contain a stale `is_active` column.
- `TaskService.update_task(...)` only normalizes updated fields and only synchronizes `status` / `completed` for explicit transitions.
- `STORAGE_SECRET` fallback is allowed only for local runs; Railway/deploy runs fail fast without it.
- Auth UI pages no longer open database sessions directly.
- Database engine creation is lazy through a central helper.
- `_ensure_task_columns()` and ad-hoc `ALTER TABLE` behavior are removed.
- Docs explain that schema-changing development updates require deleting/recreating the local SQLite DB unless a migration tool is introduced.
- Status and README no longer duplicate roadmap planning details.

## Archive Condition

Archive after implementation and verification with the repository's required checks, or document any unavailable check explicitly.
