# 070 Narrow Controller Error Handling

## Objective

Stop UI controllers from swallowing unexpected programmer errors while keeping user-facing validation errors as notifications.

## Scope

- Replace broad controller `except Exception` blocks with `except ValueError`.
- Add a focused regression test showing unexpected service errors are re-raised.

## Expected Files To Touch

- `src/student_task_manager/ui/controllers.py`
- `tests/test_task_controllers.py`

## Tests To Add Or Update

- Add or update controller tests for validation-error handling and unexpected-error propagation.

## Acceptance Criteria

- Controller validation errors still produce negative UI notifications.
- Unexpected non-validation exceptions are not hidden by the controller layer.
- Existing controller CRUD behavior remains unchanged.

## Archive Condition

- Relevant tests and repository verification gates pass.
