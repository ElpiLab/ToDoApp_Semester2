# Archive: 220 Move Task Search To Toolbar

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
- `prompts/archive/220-move-task-search-to-toolbar/prompt.md`
- `prompts/archive/220-move-task-search-to-toolbar/ARCHIVE.md`

## Tests added or updated

N/A

## Commands run

- `pytest tests/test_ui_pages.py --tb=short`
- `ruff format src\student_task_manager\ui\pages.py`
- `ruff format --check src\student_task_manager\ui\pages.py`
- `ruff check src\student_task_manager\ui\pages.py`

## Known risks and mitigations

- The search behavior is unchanged and remains title-only; this patch only moves the control to the Tasks toolbar.
- Pytest reported the known sandbox cache-write warning for `C:/Users/lence/AppData/Local/ToDoApp_Semester2/pytest_cache`; tests still passed.

## Follow-ups or rollback notes

N/A
