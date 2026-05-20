# Test Cases

This file maps the required Advanced Programming test mix to automated pytest tests.

The project has 12 rubric tests:

- 6 unit tests
- 3 database tests
- 3 integration tests

`tests/test_smoke.py` is an additional package smoke test and is not counted in the 12-test rubric mix.

## Unit Tests

| Test case ID | Automated test | Test case title/description | Preconditions | Test steps | Test data/input | Expected result | Actual result | Status | Comments |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TC_001 | `tests/test_task_service.py::test_create_task_trims_fields_and_sets_defaults` | Create task normalizes fields and applies defaults | Fake in-memory DAO is available | Create task through `TaskService` | Title and description with surrounding spaces, high priority, due date `2026-05-10` | Task is stored with trimmed fields, `created` status, and `completed=False` | Matches expected result | Pass | Unit test; no database I/O |
| TC_002 | `tests/test_task_service.py::test_update_task_marks_done_tasks_as_completed` | Updating status to done marks task completed | Existing task in fake DAO | Create task, update status to `done` | Medium-priority task | Task status is `done` and `completed=True` | Matches expected result | Pass | Covers status/completion business rule |
| TC_003 | `tests/test_task_service.py::test_update_task_reopens_completed_tasks_when_status_changes` | Reopening a completed task clears completed flag | Existing completed task in fake DAO | Create task, mark complete, update status to `pending` | Low-priority task | Task status is `pending` and `completed=False` | Matches expected result | Pass | Covers reopen behavior |
| TC_004 | `tests/test_task_service.py::test_create_task_accepts_empty_description` | Create task accepts optional description | Fake in-memory DAO is available | Create task with empty description | Title `Read chapter six`, empty description, medium priority | Task is accepted and description remains empty | Matches expected result | Pass | Documents current optional-description rule |
| TC_005 | `tests/test_task_controllers.py::test_create_task_parses_due_date_and_notifies` | Controller parses due date before calling service | Controller service is replaced by fake service | Call `create_task` controller with ISO date | Due date string `2026-05-12`, medium priority | Service receives `date(2026, 5, 12)` and success notification is emitted | Matches expected result | Pass | Unit-level controller boundary test |
| TC_006 | `tests/test_task_controllers.py::test_update_task_uses_service_boundary` | Controller update delegates through service boundary | Controller service is replaced by fake service | Call `update_task` controller | Task ID `3`, high priority, in-progress status, due date `2026-05-15` | Service receives normalized enum/date values and success notification is emitted | Matches expected result | Pass | Guards against UI-to-DAO shortcut |

## Database Tests

| Test case ID | Automated test | Test case title/description | Preconditions | Test steps | Test data/input | Expected result | Actual result | Status | Comments |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TC_007 | `tests/test_task_dao.py::test_db_create_persists_task_with_generated_id` | DAO create persists a task | Temporary SQLite database and student row exist | Create task through `TaskDAO`, read it back by ID | High-priority task due `2026-05-21` | Persisted task has generated ID and expected title/priority | Matches expected result | Pass | Uses isolated in-memory SQLite |
| TC_008 | `tests/test_task_dao.py::test_db_update_persists_status_and_completion` | DAO update persists status and completion fields | Temporary SQLite database and task exist | Create task, set done/completed, update through DAO, read back | Medium-priority task | Stored task has `done` status and `completed=True` | Matches expected result | Pass | Verifies SQL write path |
| TC_009 | `tests/test_task_dao.py::test_db_delete_removes_task` | DAO delete removes a task | Temporary SQLite database and task exist | Create task, delete through DAO, read by ID | Low-priority task | Deleted task is no longer returned | Matches expected result | Pass | Verifies delete persistence |

## Integration Tests

| Test case ID | Automated test | Test case title/description | Preconditions | Test steps | Test data/input | Expected result | Actual result | Status | Comments |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TC_010 | `tests/test_task_integration.py::test_integration_create_task_round_trips_through_database` | Service create round-trips through real DAO and SQLite | Temporary SQLite database and student row exist | Create task through `TaskService`, fetch by ID through service | Title/description with spaces, high priority, category `Project`, due date `2026-05-22` | Stored task has normalized title, description, category, and due date | Matches expected result | Pass | Integration of service + DAO + ORM |
| TC_011 | `tests/test_task_integration.py::test_integration_complete_task_updates_persisted_state` | Completing a task persists through service and DAO | Temporary SQLite database and task exist | Create task, mark complete, fetch by ID | Medium-priority task | Stored task has `done` status and `completed=True` | Matches expected result | Pass | Covers service state transition with persistence |
| TC_012 | `tests/test_task_integration.py::test_integration_filter_tasks_uses_persisted_records` | Filtering uses persisted task records | Temporary SQLite database and two tasks exist | Create high and low priority tasks, complete high task, filter open low tasks | One high-priority task and one low-priority task | Filter returns only the low-priority open task | Matches expected result | Pass | Current auth/user scoping is intentionally out of scope |
