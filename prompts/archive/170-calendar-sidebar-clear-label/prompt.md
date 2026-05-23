# 170 Calendar Sidebar Clear Label

## Scope

- Rename the calendar selected-day sidebar clear action from `Show all` to clearer wording.

## Expected files or modules to touch

- `src/student_task_manager/ui/pages.py`
- `docs/Changelog.md`
- prompt archive files for this prompt

## Tests to add or update

- No new automated test required for this copy-only UI label change.

## Acceptance criteria

- The selected-day sidebar button clearly communicates that it returns to the upcoming task list.
- Existing focused UI tests and lint/format checks still pass.

## Archive condition

- Archive after implementation and focused verification pass.
