# 280 Task View Toggle Inactive White

## Scope

- Make inactive Board/List view segments white instead of dark gray.
- Preserve the active light-green segment.

## Expected files or modules to touch

- `src/student_task_manager/ui/pages.py`
- `docs/Changelog.md`
- prompt archive files for this prompt

## Tests to add or update

- No new automated test required for styling-only UI polish.

## Acceptance criteria

- Inactive Board/List option has a white background and readable slate text.
- Active Board/List option remains light green.
- Existing focused UI tests and lint/format checks still pass.

## Archive condition

- Archive after implementation and focused verification pass.
