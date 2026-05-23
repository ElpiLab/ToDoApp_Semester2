# 190 Calendar Upcoming Header Label

## Scope

- Rename the calendar sidebar upcoming-list header from `UPCOMING` to `UPCOMING TASKS`.

## Expected files or modules to touch

- `src/student_task_manager/ui/pages.py`
- `docs/Changelog.md`
- prompt archive files for this prompt

## Tests to add or update

- No new automated test required for this copy-only UI label change.

## Acceptance criteria

- The calendar sidebar destination title matches the `Show upcoming tasks` button.
- Existing focused UI tests and lint/format checks still pass.

## Archive condition

- Archive after implementation and focused verification pass.
