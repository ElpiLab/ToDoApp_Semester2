# 340 List Badge Alignment Archive

## Date Completed

2026-05-23

## Author

Codex

## PR or Commit SHA

N/A

## Files Changed

- `src/student_task_manager/ui/pages.py`
- `docs/Changelog.md`
- `docs/Status.md`
- `prompts/archive/340-list-badge-alignment/prompt.md`
- `prompts/archive/340-list-badge-alignment/ARCHIVE.md`

## Tests Added or Updated

- N/A - layout-only class change.

## Commands Run

- `ruff format src tests`
- `pytest tests/test_ui_pages.py --tb=short`
- `pytest tests/ --tb=short`
- `ruff format --check src tests application.py`
- `ruff check src tests application.py`
- `python -m mypy src application.py`
- `python -m pip install -e ".[dev]"`

## Known Risks and Mitigations

- Pushing to `main` triggers a Railway redeploy. Without a Railway volume, demo SQLite data can reset after redeploy; recreate demo tasks after the deployment if needed.

## Follow-ups or Rollback Notes

- N/A
