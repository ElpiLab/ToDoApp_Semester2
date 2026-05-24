## Scope

Extract the Tasks page header, search, filters, and board/list toggle from `src/student_task_manager/ui/pages.py` into `src/student_task_manager/ui/tasks_page.py`.

Keep shared task state, service callbacks, navigation, and route/layout shell ownership in `pages.py`.

## Expected Files

- `src/student_task_manager/ui/pages.py`
- `src/student_task_manager/ui/tasks_page.py`
- `docs/Changelog.md`
- `docs/Roadmap.md`
- `docs/Status.md`

## Tests

- Run focused UI page tests first.
- Run the full verification gates after extraction.

## Acceptance Criteria

- Tasks header summary remains unchanged.
- Search input keeps filtering tasks by title.
- Priority and category filters keep working in board and list views.
- Status filter remains visible only in list view.
- Board/list toggle keeps switching views and preserving filter state.
- `pages.py` keeps ownership of shared state and refresh callbacks.
- No behavior change is intended.

## Archive Condition

Archive this prompt after implementation, verification, and manual smoke testing.
