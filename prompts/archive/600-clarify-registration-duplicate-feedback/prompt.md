# 600 Clarify Registration Duplicate Feedback

## Scope

Clarify registration feedback so duplicate-email handling still avoids account enumeration but does not imply a password was reset or overwritten.

## Expected Files or Modules to Touch

- `src/student_task_manager/ui/registration.py`
- `tests/test_auth_service.py`
- `tests/test_browser_smoke.py`
- relevant docs and prompt archive records

## Tests to Add or Update

- Add or update an auth regression test proving duplicate registration does not replace the existing password.
- Update browser smoke expectations for the registration page if visible text changes.

## Acceptance Criteria

- Duplicate-email registration still does not reveal whether the email exists.
- The success/info message no longer says the account definitely “has been created.”
- Tests document that duplicate registration keeps the existing password.
- Verification gates pass.

## Archive Condition

Archive after implementation, docs update, and successful verification.
