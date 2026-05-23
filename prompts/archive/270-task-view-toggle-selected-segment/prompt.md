# 270 Task View Toggle Selected Segment

## Scope

- Make the selected Board/List segment visibly distinct from the inactive segment.
- Add a subtle divider between the two view options.
- Keep existing view-switching behavior unchanged.

## Expected files or modules to touch

- `src/student_task_manager/ui/pages.py`
- `docs/Changelog.md`
- prompt archive files for this prompt

## Tests to add or update

- No new automated test required for styling-only UI polish.

## Acceptance criteria

- The active Board/List option has a visible light-green background.
- Board and List do not read as two labels on one plain white button.
- Existing focused UI tests and lint/format checks still pass.

## Archive condition

- Archive after implementation and focused verification pass.
