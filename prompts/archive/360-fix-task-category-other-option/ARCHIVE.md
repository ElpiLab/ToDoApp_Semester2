# 360 - Fix task category Other option

## Date Completed

2026-05-23

## Author

Codex

## PR or Commit SHA

N/A

## Files Changed

- `src/student_task_manager/ui/pages.py`
- `tests/test_ui_pages.py`
- `docs/Changelog.md`
- `prompts/archive/360-fix-task-category-other-option/prompt.md`
- `prompts/archive/360-fix-task-category-other-option/ARCHIVE.md`

## Tests Added or Updated

- Added `tests/test_ui_pages.py::test_task_category_options_include_other_default`.

## Commands Run

- `python -m pytest tests/test_ui_pages.py --tb=short`
- `python -m pip install -e ".[dev]"`
- `pytest tests/ --tb=short`
- `ruff format src\student_task_manager\ui\pages.py tests\test_ui_pages.py`
- `ruff format --check src tests`
- `ruff check src tests`
- `python -m mypy src`

## Known Risks and Mitigations

- Risk: The create/edit task category options could drift from the filter options later.
- Mitigation: The form now uses a named `TASK_CATEGORY_OPTIONS` constant covered by a regression test.

## Follow-ups or Rollback Notes

- N/A
