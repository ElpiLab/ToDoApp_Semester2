# 120 Simplify Settings Page Archive

## Date Completed

2026-05-20

## Author

Codex

## PR Or Commit SHA

N/A

## Files Changed

- `src/student_task_manager/ui/pages.py`
- `docs/Roadmap.md`
- `docs/Status.md`
- `docs/Changelog.md`

## Tests Added Or Updated

- N/A. UI simplification and documentation only.

## Commands Run

- `pytest tests/ --tb=short`
- `ruff format --check src tests`
- `ruff check src tests`
- `python -m mypy src`

## Known Risks And Mitigations

- Preferences, notification toggles, and appearance theme controls are no longer shown. They were not persisted, and the roadmap now records persisted preferences as future scope.
- The profile save button is disabled until the display name or email changes, then disables again after a successful save.
- The remaining destructive Settings action is labeled as "Delete all tasks" rather than app reset/account deletion.

## Follow-Ups Or Rollback Notes

- Reintroduce preference controls only after adding persistence for their values.
