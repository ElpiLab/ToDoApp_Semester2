# 260 Task View Toggle Active Background

## Scope

- Make the active Board/List view segment visibly selected with a soft green background.
- Preserve the existing switch behavior.

## Expected files or modules to touch

- `src/student_task_manager/ui/pages.py`
- `docs/Changelog.md`
- prompt archive files for this prompt

## Tests to add or update

- No new automated test required for styling-only UI polish.

## Acceptance criteria

- The active Board/List segment has a visible selected background.
- Inactive segments remain calm and readable.
- Existing focused UI tests and lint/format checks still pass.

## Archive condition

- Archive after implementation and focused verification pass.
