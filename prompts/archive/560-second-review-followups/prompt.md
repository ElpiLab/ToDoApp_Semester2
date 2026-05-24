# 560 Second Review Follow-ups

## Scope

Evaluate and implement meaningful remaining findings from the second external review after the first hardening pass.

## Expected Files or Modules to Touch

- `src/student_task_manager/services/auth_service.py`
- `src/student_task_manager/services/task_service.py`
- `src/student_task_manager/ui/controllers.py`
- `src/student_task_manager/ui/routes.py`
- `src/student_task_manager/ui/task_dialog.py`
- `src/student_task_manager/ui/tasks_page.py`
- `src/student_task_manager/ui/settings_page.py`
- `src/student_task_manager/ui/view_helpers.py`
- `src/student_task_manager/ui/notifications.py`
- relevant tests under `tests/`
- relevant docs and prompt archive records

## Tests to Add or Update

- Controller test for rejecting boolean `user_id` session values.
- Service tests for email-change re-authentication and duplicate-email rollback.
- UI helper or page tests for shared email validation and label consistency.
- Tests for status/filter behavior where practical without adding brittle UI coupling.

## Acceptance Criteria

- Remaining meaningful review suggestions are either implemented or documented as not applicable.
- Service-layer validation remains the source of truth.
- Auth-sensitive email changes require current password.
- Batch task deletion avoids notification spam.
- Board view is not silently filtered by hidden List status state.
- Prompt and docs are updated, then archived after verification.

## Archive Condition

Archive after implementation and successful verification.
