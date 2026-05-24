# Archive: 500 Clean Root and Persistence Contract

## Date Completed

2026-05-24

## Author

Codex

## PR or Commit SHA

N/A

## Files Changed

- `.vscode/settings.json`
- `README.md`
- `application.py`
- `docs/Changelog.md`
- `docs/Roadmap.md`
- `docs/Status.md`
- `docs/architecture/erd.dbml`
- `docs/architecture/erd.drawio`
- `docs/architecture/erd.png`
- `src/student_task_manager/data_access/dao.py`
- `src/student_task_manager/data_access/db.py`
- `src/student_task_manager/services/task_service.py`
- `src/student_task_manager/ui/login.py`
- `src/student_task_manager/ui/registration.py`
- `src/student_task_manager/ui/routes.py`
- `src/student_task_manager/ui/tasks_page.py`
- `tests/test_db_config.py`
- `tests/test_task_controllers.py`
- `tests/test_task_dao.py`
- `tests/test_task_integration.py`
- `tests/test_task_service.py`
- `prompts/archive/500-clean-root-and-persistence-contract/prompt.md`
- removed `erd.dbml`, `erd.drawio`, `erd.png`, and `procfile.txt` from the repository root

## Tests Added or Updated

- Updated database config expectations for `sqlite:///data/todo.db`.
- Updated DAO tests to use scoped task lookup methods.
- Removed integration coverage for the deleted `TaskService.filter_tasks()` API.
- Cleaned controller test doubles so unused-argument linting stays quiet.

## Commands Run

- `python -m pip install -e ".[dev]"`
- `pytest tests/ --tb=short`
- `ruff format src tests`
- `ruff format --check src tests`
- `ruff check src tests`
- `python -m mypy src`
- `python -m ruff check src tests --select F401,F841,F811,ARG --preview --no-cache`

## Known Risks and Mitigations

- Local app process `python.exe application.py` was stopped before moving `todo.db` to `data/todo.db`.
- `pytest` reports a cache write warning under `C:/Users/lence/AppData/Local/ToDoApp_Semester2/pytest_cache`; tests still pass.
- Route registration is now explicit from `application.py`; existing import-time side effects are removed.

## Follow-ups or Rollback Notes

- Registration still contains UI-level persistence and should be moved behind `AuthService` in a future cleanup.
- If a rollback is needed, restore the default database URL to `sqlite:///todo.db` and move `data/todo.db` back to the repository root.
