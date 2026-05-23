# 360 - Fix task category Other option

## Scope

Ensure the task create/edit form includes the built-in `Other` category option so users can select it directly instead of having to type it.

## Expected Files

- `src/student_task_manager/ui/pages.py`
- `tests/test_ui_pages.py`

## Tests

- Add or update a focused UI helper test that verifies the built-in task category options include `Other`.
- Run the relevant test file first, then the repository verification gates as practical.

## Acceptance Criteria

- The task create/edit category dropdown includes `Other`.
- Existing custom category behavior remains intact.
- Existing category filter behavior is unchanged.

## Archive Condition

Archive this prompt after the code change is implemented, verified, and documented if needed.
