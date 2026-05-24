# Test Cases

This file maps the required Advanced Programming test mix to automated pytest tests.

The project has 12 rubric tests:

- 6 unit tests
- 3 database tests
- 3 integration tests

`tests/test_smoke.py` and `tests/test_browser_smoke.py` are additional smoke tests and are not counted in the 12-test rubric mix. The suite also includes extra auth/user-scope and hardening regression tests beyond the 12 required rubric tests.

## Unit Tests

| Test case ID | Automated test | Test case title/description | Preconditions | Test steps | Test data/input | Expected result | Actual result | Status | Comments |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TC_001 | `tests/test_task_service.py::test_create_task_trims_fields_and_sets_defaults` | Create task normalizes fields and applies defaults | Fake in-memory DAO is available | Create task through `TaskService` | User ID `7`, title and description with surrounding spaces, high priority, due date `2026-05-10` | Task is stored with trimmed fields, `pending` status, `completed=False`, and `user_id=7` | Matches expected result | Pass | Unit test; no database I/O |
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
| TC_010 | `tests/test_task_integration.py::test_integration_create_task_round_trips_through_database` | Service create round-trips through real DAO and SQLite | Temporary SQLite database and student row exist | Create task through `TaskService`, fetch by ID through service for the same user | User ID `1`, title/description with spaces, high priority, category `Project`, due date `2026-05-22` | Stored task has normalized title, description, category, due date, and owner | Matches expected result | Pass | Integration of service + DAO + ORM |
| TC_011 | `tests/test_task_integration.py::test_integration_complete_task_updates_persisted_state` | Completing a task persists through service and DAO | Temporary SQLite database and task exist | Create task, mark complete, fetch by ID | Medium-priority task | Stored task has `done` status and `completed=True` | Matches expected result | Pass | Covers service state transition with persistence |
| TC_012 | `tests/test_task_integration.py::test_integration_other_user_cannot_update_task` | Service and DAO reject cross-user task updates | Temporary SQLite database and a task owned by user ID `1` exist | Create a task as user ID `1`, attempt to update it as user ID `2`, then fetch it as user ID `1` | User ID `1` task and unauthorized update request from user ID `2` | Unauthorized update raises `Task not found`, and the original task remains unchanged | Matches expected result | Pass | Confirms authenticated task ownership across service + DAO + ORM |

## Additional Regression Tests

These tests are intentionally outside the 12-test rubric count. They protect authenticated-user behavior, validation boundaries, deployment safeguards, and UI helper formatting added after the rubric-alignment pass.

| Automated test | Purpose | Status |
| --- | --- | --- |
| `tests/test_task_service.py::test_get_all_tasks_returns_only_requested_user_tasks` | Service list operations return only the requested user's tasks | Pass |
| `tests/test_task_service.py::test_update_task_rejects_other_users_task` | Service update path rejects cross-user access with `Task not found` | Pass |
| `tests/test_task_service.py::test_update_task_rejects_invalid_priority_before_persistence` | Service rejects invalid priority values before DAO writes | Pass |
| `tests/test_task_service.py::test_update_task_rejects_invalid_status_before_persistence` | Service rejects invalid status values before DAO writes | Pass |
| `tests/test_task_service.py::test_update_task_rejects_non_boolean_completed` | Service rejects non-boolean completion values | Pass |
| `tests/test_task_service.py::test_delete_all_tasks_removes_only_requested_users_tasks` | Batch deletion removes only the authenticated user's tasks | Pass |
| `tests/test_task_integration.py::test_integration_invalid_priority_update_does_not_corrupt_row` | Invalid enum updates do not corrupt persisted SQLite rows | Pass |
| `tests/test_task_controllers.py::test_create_task_requires_logged_in_user` | Controller task creation fails clearly when no user is logged in | Pass |
| `tests/test_task_controllers.py::test_current_user_id_rejects_boolean_session_values` | Controller ownership lookup rejects boolean session IDs | Pass |
| `tests/test_task_controllers.py::test_delete_all_tasks_uses_single_success_notification` | Batch deletion emits one success notification instead of one per task | Pass |
| `tests/test_task_dao.py::test_db_user_scoped_queries_hide_other_users_tasks` | DAO user-scoped list/fetch methods hide another user's tasks | Pass |
| `tests/test_task_dao.py::test_db_delete_all_for_user_removes_only_owned_tasks` | DAO batch deletion stays scoped to one owner | Pass |
| `tests/test_auth_service.py::test_update_profile_validates_input` | Auth service owns profile name and email validation | Pass |
| `tests/test_auth_service.py::test_update_profile_requires_current_password_for_email_change` | Email changes require current-password re-authentication | Pass |
| `tests/test_auth_service.py::test_update_profile_rejects_wrong_current_password_for_email_change` | Email changes reject incorrect current passwords | Pass |
| `tests/test_auth_service.py::test_update_profile_rejects_duplicate_email_change` | Profile email changes reject duplicate addresses | Pass |
| `tests/test_auth_service.py::test_update_profile_normalizes_email_case` | Profile updates normalize email case before persistence | Pass |
| `tests/test_auth_service.py::test_register_validates_input` | Registration rejects invalid names, emails, mismatched passwords, passwords shorter than 10 characters, and passwords over 72 bytes | Pass |
| `tests/test_auth_service.py::test_change_password_rejects_short_new_password` | Password changes reject replacement passwords shorter than 10 characters | Pass |
| `tests/test_auth_service.py::test_change_password_rejects_long_new_password` | Password changes reject bcrypt inputs over 72 bytes | Pass |
| `tests/test_auth_service.py::test_login_throttles_repeated_failed_attempts` | Repeated failed logins are temporarily throttled | Pass |
| `tests/test_auth_service.py::test_login_success_resets_throttle` | Successful login resets prior failure count | Pass |
| `tests/test_auth_service.py::test_login_normalizes_email_case` | Login normalizes email case and surrounding whitespace | Pass |
| `tests/test_application.py::test_storage_secret_rejects_missing_secret_for_public_host` | Public-host runs cannot use the development storage secret | Pass |
| `tests/test_application.py::test_storage_secret_allows_localhost_host_fallback` | Localhost runs can still use the local development fallback | Pass |
| `tests/test_application.py::test_create_dev_admin_if_enabled_is_idempotent` | Development admin bootstrap tolerates an existing account | Pass |
| `tests/test_notifications.py::test_notification_key_rejects_unpersisted_task_id` | Notification keys reject unpersisted task IDs instead of falling back to zero | Pass |
| `tests/test_task_dialog.py::test_status_options_are_flat_three_state_options` | Task dialog status options match the three persisted task states | Pass |
| `tests/test_ui_pages.py::test_filter_visible_tasks_ignores_hidden_status_filter_in_board_view` | Hidden List status filters do not silently filter Board view | Pass |
| `tests/test_ui_pages.py::test_filter_visible_tasks_applies_status_filter_in_list_view` | List view still applies the visible status filter | Pass |
| `tests/test_ui_pages.py::test_relative_due_text_uses_ascii_separator` | Relative due-date text avoids mojibake in visible labels | Pass |
| `tests/test_browser_smoke.py::test_simulated_browser_can_open_login_page` | NiceGUI simulated user can render the login page | Pass |
| `tests/test_browser_smoke.py::test_simulated_browser_can_open_registration_page` | NiceGUI simulated user can render the registration page | Pass |
