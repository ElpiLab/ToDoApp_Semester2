# 320 Status Label Consistency Archive

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
- `docs/Status.md`
- `prompts/archive/320-status-label-consistency/prompt.md`
- `prompts/archive/320-status-label-consistency/ARCHIVE.md`

## Tests Added or Updated

- Added `test_status_display_label_uses_consistent_task_status_terms` to cover the shared status label mapping.

## Commands Run

- `pytest tests/test_ui_pages.py --tb=short`
- `ruff format src tests`
- `pytest tests/ --tb=short`
- `ruff format --check src tests application.py`
- `ruff check src tests application.py`
- `python -m mypy src application.py`
- `python -m pip install -e ".[dev]"`

## Known Risks and Mitigations

- Railway still uses ephemeral storage unless a volume is attached. Pushing this change will redeploy the app and can reset demo tasks; recreate demo data after the deploy if needed.

## Follow-ups or Rollback Notes

- N/A
