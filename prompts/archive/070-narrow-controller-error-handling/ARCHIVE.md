# 070 Narrow Controller Error Handling Archive

## Date Completed

2026-05-20

## Author

Codex

## PR Or Commit SHA

N/A

## Files Changed

- `src/student_task_manager/ui/controllers.py`
- `tests/test_task_controllers.py`

## Tests Added Or Updated

- Added a controller regression test proving unexpected service errors are re-raised instead of hidden behind a UI notification.
- Kept the existing login-required validation notification test.

## Commands Run

- `pytest tests/test_task_controllers.py --tb=short`
- `pytest tests/ --tb=short`
- `ruff format --check src tests`
- `ruff check src tests`
- `python -m mypy src`

## Known Risks And Mitigations

- Unexpected controller errors now propagate instead of returning `None`, `False`, or `[]`. This is intentional so programming errors are visible during development.
- User-facing validation failures still raise `ValueError` and continue to show negative UI notifications.

## Follow-Ups Or Rollback Notes

- N/A
