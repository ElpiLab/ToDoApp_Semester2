# Archive: 200 Calendar Sidebar Back Label

## Date completed

2026-05-23

## Author

Codex

## PR or commit SHA

N/A

## Files changed

- `src/student_task_manager/ui/pages.py`
- `docs/Changelog.md`
- `docs/Status.md`
- `prompts/archive/200-calendar-sidebar-back-label/prompt.md`
- `prompts/archive/200-calendar-sidebar-back-label/ARCHIVE.md`

## Tests added or updated

N/A

## Commands run

- `pytest tests/test_ui_pages.py --tb=short`
- `ruff format src\student_task_manager\ui\pages.py`
- `ruff format --check src\student_task_manager\ui\pages.py`
- `ruff check src\student_task_manager\ui\pages.py`

## Known risks and mitigations

- This is a copy-only UI label change.
- Pytest reported the known sandbox cache-write warning for `C:/Users/lence/AppData/Local/ToDoApp_Semester2/pytest_cache`; tests still passed.

## Follow-ups or rollback notes

N/A
