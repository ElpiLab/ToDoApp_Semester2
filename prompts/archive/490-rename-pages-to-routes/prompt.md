# 490 Rename pages module to routes

## Scope

Rename the remaining NiceGUI route orchestration module from `pages.py` to `routes.py` so the file name matches its current responsibility after the UI split.

## Expected files

- `src/student_task_manager/ui/pages.py`
- `src/student_task_manager/ui/routes.py`
- `application.py`
- `README.md`
- `docs/Changelog.md`

## Tests

- Run focused import/route tests if available.
- Run formatting, linting, and type checks for touched files.

## Acceptance criteria

- The app imports route registrations from `student_task_manager.ui.routes`.
- No runtime references to `student_task_manager.ui.pages` remain outside historical prompt/archive documentation.
- README project structure names `routes.py`.
- Behavior is unchanged.

## Archive condition

Archive after the rename is complete and focused verification passes.
