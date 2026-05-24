# 490 Rename pages module to routes

## Date completed

2026-05-24

## Author

Codex

## PR or commit SHA

N/A

## Files changed

- `application.py`
- `README.md`
- `docs/Changelog.md`
- `src/student_task_manager/ui/pages.py`
- `src/student_task_manager/ui/routes.py`
- `prompts/archive/490-rename-pages-to-routes/prompt.md`
- `prompts/archive/490-rename-pages-to-routes/ARCHIVE.md`

## Tests added or updated

N/A

## Commands run

- `pytest tests\test_application.py tests\test_ui_pages.py --tb=short`
- `ruff format application.py`
- `ruff format --check application.py src\student_task_manager\ui\routes.py src\student_task_manager\ui\app_shell.py src\student_task_manager\ui\controllers.py src\student_task_manager\deployment.py`
- `ruff check application.py src\student_task_manager\ui\routes.py src\student_task_manager\ui\app_shell.py src\student_task_manager\ui\controllers.py src\student_task_manager\deployment.py`
- `python -m mypy application.py src\student_task_manager\ui\routes.py src\student_task_manager\ui\app_shell.py src\student_task_manager\ui\controllers.py src\student_task_manager\deployment.py`

## Known risks and mitigations

- Risk: A stale import could prevent NiceGUI route registration at startup.
- Mitigation: Updated the launcher import and ran focused application/UI tests plus type, format, and lint checks.

## Follow-ups or rollback notes

- Roll back by renaming `routes.py` back to `pages.py` and restoring the launcher import.
