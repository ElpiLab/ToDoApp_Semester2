# 380 Extract UI View Helpers

## Scope

Reduce the size of `pages.py` by extracting pure UI helper constants and formatting/filter functions into a separate module.

This is Phase 1 of the UI split plan. Do not move page renderers or NiceGUI callback-heavy logic in this prompt.

## Expected Files

- `src/student_task_manager/ui/pages.py`
- `src/student_task_manager/ui/view_helpers.py`
- `tests/test_ui_pages.py`
- `docs/Changelog.md`
- `docs/Status.md`

## Tests

- Update helper tests to import from `student_task_manager.ui.view_helpers`.
- Run:
  - `pytest tests/test_ui_pages.py --tb=short`
  - `pytest tests/ --tb=short`
  - `ruff format --check src tests`
  - `ruff check src tests`
  - `python -m mypy src`

## Acceptance Criteria

- `pages.py` no longer owns pure helper constants/functions.
- App behavior is unchanged.
- Existing UI helper tests pass against the new helper module.
- Full verification passes.

## Archive Condition

Archive after the extraction is complete, verification passes, and relevant docs record the change.
