# 570 Auth Throttling and Cleanups

## Scope

Finish the remaining auth and cleanup requests: remove the email-validation UI wrapper, add login throttling, avoid duplicate-email registration enumeration, raise the password floor to 10 characters, and evaluate small structural cleanup suggestions.

## Expected Files or Modules to Touch

- `src/student_task_manager/services/auth_service.py`
- `src/student_task_manager/ui/registration.py`
- `src/student_task_manager/ui/settings_page.py`
- `src/student_task_manager/ui/view_helpers.py`
- `src/student_task_manager/ui/dashboard_page.py`
- relevant tests and docs

## Tests to Add or Update

- Auth service tests for login throttling and generic duplicate-email registration.
- Existing password validation tests updated to the 10-character floor.
- Existing email validation imports updated to use the domain helper directly.

## Acceptance Criteria

- UI code imports `is_valid_email` from `domain.validation` directly.
- Repeated failed login attempts are temporarily throttled.
- Duplicate-email registration does not produce a distinct user-facing registration outcome.
- Registration and password changes require at least 10 characters and still enforce the bcrypt byte limit.
- Dashboard quick-complete no longer re-renders by directly recursing inside the dashboard renderer.
- Engine disposal and PageContext dataclasses are evaluated and either implemented or documented as not worth this patch.

## Archive Condition

Archive after implementation, docs update, and successful verification.
