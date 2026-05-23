# 200 Calendar Sidebar Back Label

## Scope

- Rename the calendar selected-day sidebar action from `Show upcoming tasks` to `Back to upcoming tasks`.

## Expected files or modules to touch

- `src/student_task_manager/ui/pages.py`
- `docs/Changelog.md`
- prompt archive files for this prompt

## Tests to add or update

- No new automated test required for this copy-only UI label change.

## Acceptance criteria

- The selected-day sidebar action clearly communicates that it exits the date-specific view and returns to the upcoming task list.
- Existing focused UI tests and lint/format checks still pass.

## Archive condition

- Archive after implementation and focused verification pass.
