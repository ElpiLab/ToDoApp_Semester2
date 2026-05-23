# 220 Move Task Search To Toolbar

## Scope

- Move the `Search tasks...` input from the global header into the Tasks page toolbar.
- Keep existing live title-filter behavior.

## Expected files or modules to touch

- `src/student_task_manager/ui/pages.py`
- `docs/Changelog.md`
- prompt archive files for this prompt

## Tests to add or update

- No new automated test required for moving an existing UI control without changing filtering logic.

## Acceptance criteria

- Header no longer shows the task search input.
- Tasks page toolbar shows `Search tasks...`.
- Search still updates `state["search"]` and calls `refresh_tasks()`.
- Existing focused UI tests and lint/format checks still pass.

## Archive condition

- Archive after implementation and focused verification pass.
