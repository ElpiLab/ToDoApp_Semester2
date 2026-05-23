# Archive: 150 Auth Service Hardening

## Date completed

2026-05-23

## Author

Codex

## PR or commit SHA

N/A

## Files changed

- `src/student_task_manager/services/auth_service.py`
- `tests/test_auth_service.py`
- `docs/Status.md`
- `prompts/archive/150-auth-service-hardening/prompt.md`
- `prompts/archive/150-auth-service-hardening/ARCHIVE.md`

## Tests added or updated

- Added `tests/test_auth_service.py::test_change_password_rejects_short_new_password`
- Added `tests/test_auth_service.py::test_change_password_rejects_reusing_current_password`
- Updated existing password-change auth tests to use passwords that satisfy the minimum length rule.

## Commands run

- `pytest tests/test_auth_service.py --tb=short`
- `pytest tests/ --tb=short`
- `ruff format src\student_task_manager\services\auth_service.py tests\test_auth_service.py`
- `ruff format --check src tests`
- `ruff check src tests`
- `python -m mypy src`
- `python -m pip install -e ".[dev]"`

## Known risks and mitigations

- Registration still writes directly from `ui/registration.py`; this is a known pre-existing boundary issue. It was left unchanged to avoid destabilizing the working registration flow before upload.
- Pytest reported a cache-write warning under the sandbox for `C:/Users/lence/AppData/Local/ToDoApp_Semester2/pytest_cache`; tests still passed.

## Follow-ups or rollback notes

- Follow up by moving `/register` persistence and validation behind `AuthService`.
- Rollback is limited to restoring the removed `AuthService.register` method and service-level password validation if an external caller is discovered, but local grep found no callers in `src` or `tests`.
