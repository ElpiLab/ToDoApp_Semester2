# Prompt 520 Archive: Lazy DB and Auth Boundaries

## Date Completed

2026-05-24

## Author

Codex

## PR or Commit SHA

N/A

## Files Changed

- `application.py`
- `src/student_task_manager/data_access/db.py`
- `src/student_task_manager/data_access/dao.py`
- `src/student_task_manager/deployment.py`
- `src/student_task_manager/services/auth_service.py`
- `src/student_task_manager/services/task_service.py`
- `src/student_task_manager/ui/login.py`
- `src/student_task_manager/ui/registration.py`
- `src/student_task_manager/ui/settings_page.py`
- `tests/conftest.py`
- `tests/test_application.py`
- `tests/test_auth_service.py`
- `tests/test_db_config.py`
- `tests/test_task_dao.py`
- `tests/test_task_integration.py`
- `tests/test_task_service.py`
- `README.md`
- `docs/Status.md`
- `docs/Roadmap.md`
- `docs/Changelog.md`
- `AGENTS.md`
- `data/todo.db`

## Tests Added or Updated

- Added task update regressions for status-only updates on legacy short titles.
- Added task update regression for `completed=False` on an in-progress task.
- Added auth regressions for empty credentials and malformed stored password hashes.
- Added deployment secret tests for local fallback and deployed fail-fast behavior.
- Added a DB helper regression proving lazy SQLite parent directory creation.

## Commands Run

```bash
python -m pip install -e ".[dev]"
pytest tests/test_auth_service.py tests/test_task_service.py tests/test_task_dao.py tests/test_task_integration.py tests/test_application.py --tb=short
ruff check src tests --select F401,F841,F811,ARG --preview --no-cache
ruff format src tests
pytest tests/ --tb=short
ruff format --check src tests
ruff check src tests
python -m mypy src
```

## Known Risks and Mitigations

- Existing non-local SQLite databases may still contain columns from earlier development schemas. This project still has no migration tool, so development schema changes are handled by deleting and recreating SQLite databases from ORM metadata.
- `pytest` completed with a cache write warning for `C:/Users/lence/AppData/Local/ToDoApp_Semester2/pytest_cache`; test results were otherwise green.

## Follow-ups or Rollback Notes

- Introduce Alembic before preserving existing deployed SQLite data across schema-changing releases.
- The Roadmap remains the place for future scope; Status should stay current-state only.
