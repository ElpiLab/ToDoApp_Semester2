# 380 Extract UI View Helpers Archive

## Date Completed

2026-05-23

## Author

Codex

## PR or Commit SHA

N/A

## Files Changed

- `src/student_task_manager/ui/pages.py`
- `src/student_task_manager/ui/view_helpers.py`
- `tests/test_ui_pages.py`
- `docs/Changelog.md`
- `docs/Roadmap.md`
- `docs/Status.md`
- `prompts/archive/380-extract-ui-view-helpers/prompt.md`
- `prompts/archive/380-extract-ui-view-helpers/ARCHIVE.md`

## Tests Added or Updated

- Updated `tests/test_ui_pages.py` so pure helper tests import from `student_task_manager.ui.view_helpers`.

## Commands Run

- `pytest tests/test_ui_pages.py --tb=short`
- `pytest tests/ --tb=short`
- `ruff format src tests`
- `ruff format --check src tests`
- `ruff check src tests`
- `python -m mypy src`
- `python -m pip install -e ".[dev]"`

## Known Risks and Mitigations

- Risk: Import movement could break UI render paths that still depend on helper names.
- Mitigation: `pages.py` imports the same names from `view_helpers.py`; focused helper tests and the full test suite passed.

## Follow-Ups or Rollback Notes

- Continue the UI split later by extracting page renderers and shared components from `pages.py`.
- Rollback is straightforward: move helper definitions back into `pages.py` and point tests back to `student_task_manager.ui.pages`.
