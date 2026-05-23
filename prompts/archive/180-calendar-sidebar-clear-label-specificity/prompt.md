# 180 Calendar Sidebar Clear Label Specificity

## Scope

- Rename the calendar selected-day sidebar clear action from `Show upcoming` to `Show upcoming tasks`.

## Expected files or modules to touch

- `src/student_task_manager/ui/pages.py`
- `docs/Changelog.md`
- prompt archive files for this prompt

## Tests to add or update

- No new automated test required for this copy-only UI label change.

## Acceptance criteria

- The selected-day sidebar button clearly says it returns to upcoming tasks.
- Existing focused UI tests and lint/format checks still pass.

## Archive condition

- Archive after implementation and focused verification pass.
