# 330 Task Status Filter Consistency

## Scope

Fix the Tasks List status filter so it matches the visible task statuses: "To do", "In Progress", and "Done". Remove remaining user-facing "open" wording from the Tasks header summary when it is counting all unfinished tasks.

## Expected Files

- `src/student_task_manager/ui/pages.py`
- `tests/test_ui_pages.py`
- `docs/Changelog.md`
- `docs/Status.md`

## Tests

- Add a focused regression test for status-filter matching.
- Run the relevant UI test module and the full verification gates.

## Acceptance Criteria

- List-view Status filter options are All / To do / In Progress / Done.
- Selecting To do does not include In Progress tasks.
- Selecting In Progress shows only unfinished in-progress tasks.
- Selecting Done includes completed tasks.
- The Tasks header summary uses "active" instead of "open" for unfinished-task counts.

## Archive Condition

Archive this prompt after implementation, verification, documentation updates, commit, and push are complete.
