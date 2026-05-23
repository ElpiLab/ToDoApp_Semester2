# 030 Auth User Scope Cleanup

## Objective

Make task ownership explicit throughout the task stack so authenticated users only create, read, update, complete, reopen, and delete their own tasks. Remove the current hidden `user_id=1` behavior from normal task operations.

## Scope

- add user-scoped DAO methods for listing and fetching tasks
- update `TaskService` methods to require `user_id` for task operations
- update UI controllers to read the authenticated user ID from NiceGUI user storage and pass it to the service layer
- fail clearly when a task operation is attempted without an authenticated user
- update existing tests for the new method signatures
- add regression tests for per-user task isolation
- update `docs/Status.md`, `docs/Changelog.md`, `docs/Roadmap.md`, and `docs/TestCases.md` if the test mapping changes
- do not redesign the login page, registration page, password hashing, or profile UI in this prompt except where required to pass the authenticated user ID into task operations
- do not add new domain entities or migrations in this prompt

## Expected files or modules to touch

- `src/student_task_manager/data_access/dao.py`
- `src/student_task_manager/services/task_service.py`
- `src/student_task_manager/ui/controllers.py`
- `src/student_task_manager/ui/pages.py` only if controller call sites require adjustment
- `tests/test_task_service.py`
- `tests/test_task_dao.py`
- `tests/test_task_integration.py`
- `tests/test_task_controllers.py`
- `docs/Status.md`
- `docs/Changelog.md`
- `docs/Roadmap.md`
- `docs/TestCases.md`

## Tests to add or update

- service test proving created tasks store the provided `user_id`
- DAO test proving user-scoped list/fetch methods do not return another user's tasks
- integration test proving service operations cannot update or delete another user's task
- controller test proving task actions fail clearly without a logged-in user
- update existing tests to pass explicit `user_id`

## Acceptance criteria

- no normal task operation in `TaskService` hardcodes `user_id=1`
- task reads and writes are scoped to the authenticated user
- attempting to access another user's task returns the existing "Task not found" path or another explicit validation error
- `pytest tests/ --tb=short` passes
- `ruff format --check src tests` passes
- `ruff check src tests` passes
- `python -m mypy src` passes
- planning docs no longer list auth/user scoping as an unresolved task-ownership gap

## Archive condition

Archive this prompt only when user-scoped task behavior is implemented, regression-tested, documented, and verified.
