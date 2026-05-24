# Archive: 510 Auth and Contract Hardening

## Date Completed

2026-05-24

## Author

Codex

## PR or Commit SHA

N/A

## Files Changed

- `.vscode/settings.json`
- `AGENTS.md`
- `README.md`
- `application.py`
- `docs/Changelog.md`
- `docs/Roadmap.md`
- `docs/Status.md`
- `docs/TestCases.md`
- `src/student_task_manager/data_access/dao.py`
- `src/student_task_manager/deployment.py`
- `src/student_task_manager/domain/models.py`
- `src/student_task_manager/services/auth_service.py`
- `src/student_task_manager/services/task_service.py`
- `src/student_task_manager/ui/registration.py`
- `tests/test_application.py`
- `tests/test_auth_service.py`
- `tests/test_task_dao.py`
- `tests/test_task_service.py`
- `prompts/archive/510-auth-and-contract-hardening/prompt.md`

## Tests Added or Updated

- Added dev-admin configuration tests.
- Added `AuthService.register(...)` validation and duplicate-email tests.
- Added `AuthService.update_profile(...)` missing-user test.
- Added DAO regression coverage for scoped deletion.
- Updated task-service fake DAO behavior for `delete_for_user(...)`.

## Commands Run

- `python -m pip install -e ".[dev]"`
- `pytest tests/test_application.py tests/test_auth_service.py tests/test_task_dao.py tests/test_task_service.py --tb=short`
- `pytest tests/ --tb=short`
- `ruff format src tests`
- `ruff format --check src tests`
- `ruff check src tests`
- `python -m mypy src`
- `python -m ruff check src tests --select F401,F841,F811,ARG --preview --no-cache`

## Known Risks and Mitigations

- `pytest` still reports a cache write warning under `C:/Users/lence/AppData/Local/ToDoApp_Semester2/pytest_cache`; the test suite passes.
- `runtime.txt` remains pinned to `python-3.11.9` because project tooling targets Python 3.11. The local interpreter used for verification is Python 3.13.5.
- Existing databases may retain an unused `is_active` column because the project bootstraps schema with `create_all` and does not run destructive migrations.

## Follow-ups or Rollback Notes

- If inactive-user lifecycle management becomes in scope, add an explicit model field and tests through a new prompt.
- To roll back dev-admin hardening, restore the old startup seed path, but avoid reintroducing static credentials in production.
