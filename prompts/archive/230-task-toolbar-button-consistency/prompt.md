# 230 Task Toolbar Button Consistency

## Scope

- Make task controls more visually and textually consistent.
- Keep behavior unchanged.

## Expected files or modules to touch

- `src/student_task_manager/ui/pages.py`
- `docs/Status.md`
- `docs/Changelog.md`
- prompt archive files for this prompt

## Tests to add or update

- No new automated test required for copy/styling-only UI polish.

## Acceptance criteria

- The header task creation button uses sentence case consistently with other command buttons.
- The Tasks page Board/List toggle reads as a segmented control.
- Status documentation reflects that task search lives in the Tasks toolbar, not the global header.
- Existing focused UI tests and lint/format checks still pass.

## Archive condition

- Archive after implementation and focused verification pass.
