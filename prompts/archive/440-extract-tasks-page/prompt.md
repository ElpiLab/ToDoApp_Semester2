## Scope

Extract the task board and list rendering from `src/student_task_manager/ui/pages.py` into a focused `src/student_task_manager/ui/tasks_page.py` module.

Keep the main page shell, routing, filters, search state, notification drawer, and task dialog wiring in `pages.py`.

## Expected Files

- `src/student_task_manager/ui/pages.py`
- `src/student_task_manager/ui/tasks_page.py`
- `docs/Changelog.md`
- `docs/Roadmap.md`
- `docs/Status.md`

## Tests

- Run the UI page tests first.
- Run the full verification gates after the extraction.

## Acceptance Criteria

- Task board rendering is moved out of `pages.py`.
- Task list rendering is moved out of `pages.py`.
- Board/list toggle, filters, search, task edit, task completion, task deletion, status menu, and drag/drop still work.
- `pages.py` keeps ownership of shared state and service callbacks.
- No behavior change is intended.

## Archive Condition

Archive this prompt after implementation, verification, and manual smoke testing.
