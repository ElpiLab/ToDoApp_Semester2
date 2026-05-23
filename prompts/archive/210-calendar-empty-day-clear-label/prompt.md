# 210 Calendar Empty Day Clear Label

## Scope

- Make the calendar selected-day sidebar clear action label depend on whether the selected day has tasks.

## Expected files or modules to touch

- `src/student_task_manager/ui/pages.py`
- `docs/Changelog.md`
- prompt archive files for this prompt

## Tests to add or update

- No new automated test required for this small copy-only conditional label.

## Acceptance criteria

- Empty selected days show `Show upcoming tasks`.
- Selected days with tasks show `Back to upcoming tasks`.
- The action still clears the selected-day filter and returns to `UPCOMING TASKS`.
- Existing focused UI tests and lint/format checks still pass.

## Archive condition

- Archive after implementation and focused verification pass.
