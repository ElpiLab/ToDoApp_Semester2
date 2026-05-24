# 480 Add intent-level comments

## Scope

Add a small number of useful comments/docstrings that explain non-obvious architectural intent after the UI extraction work.

## Expected files

- `src/student_task_manager/ui/pages.py`
- `src/student_task_manager/ui/app_shell.py`
- `src/student_task_manager/ui/controllers.py`
- `src/student_task_manager/deployment.py`

## Tests

- Run formatting, linting, and type checks for touched files.
- Full test suite is not required because this is comment-only, unless an edit accidentally changes executable code.

## Acceptance criteria

- Comments explain intent or constraints that help a new developer.
- No obvious comments that restate individual statements.
- No behavior changes.

## Archive condition

Archive after comments are added and touched-file checks pass.
