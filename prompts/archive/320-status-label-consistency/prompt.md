# 320 Status Label Consistency

## Scope

Make user-facing task status labels consistently use "To do", "In Progress", and "Done" instead of mixing "Open" and "To do".

## Expected Files

- `src/student_task_manager/ui/pages.py`
- `tests/test_ui_pages.py`
- `docs/Changelog.md`
- `docs/Status.md`

## Tests

- Add or update focused UI label tests where practical.
- Run the full automated suite plus formatting, lint, and mypy checks.

## Acceptance Criteria

- Tasks List section headers use "To do", "In Progress", and "Done".
- Task status pills and status menus use "To do" for not-started tasks.
- Analytics status labels use "To do" instead of "Open" where they represent a task status.
- Non-status wording like "active tasks" may remain unchanged.

## Archive Condition

Archive this prompt after implementation, verification, and documentation updates are complete.
