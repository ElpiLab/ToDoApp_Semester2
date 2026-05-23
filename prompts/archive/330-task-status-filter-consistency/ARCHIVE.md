# 330 Task Status Filter Consistency Archive

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
- `prompts/archive/330-task-status-filter-consistency/prompt.md`
- `prompts/archive/330-task-status-filter-consistency/ARCHIVE.md`

## Tests Added or Updated

- Added `test_task_matches_status_filter_matches_visible_status_sections`.

## Commands Run

- `pytest tests/test_ui_pages.py --tb=short`
- `ruff format src tests`
- `pytest tests/ --tb=short`
- `ruff format --check src tests application.py`
- `ruff check src tests application.py`
- `python -m mypy src application.py`
- `python -m pip install -e ".[dev]"`

## Known Risks and Mitigations

- Pushing to `main` triggers a Railway redeploy. Without a Railway volume, demo SQLite data can reset after redeploy; recreate demo tasks after the deployment if needed.

## Follow-ups or Rollback Notes

- N/A
