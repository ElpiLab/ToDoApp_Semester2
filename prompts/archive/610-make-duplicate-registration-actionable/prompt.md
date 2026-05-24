# 610 Make Duplicate Registration Actionable

## Scope

Make duplicate registration feedback actionable in the deployed app without claiming that an account was created or that a password was changed.

## Expected Files or Modules to Touch

- `src/student_task_manager/ui/registration.py`
- `tests/test_auth_service.py`
- relevant docs and prompt archive records

## Tests to Add or Update

- Keep the duplicate-registration password preservation regression test.
- Add focused coverage only if the UI control flow is easy to test without brittle NiceGUI internals.

## Acceptance Criteria

- Successful new registration still navigates to login.
- Duplicate registration does not navigate to login and does not imply success.
- Duplicate registration message tells the user to use the existing password or another email without exposing passwords.
- Verification gates pass.

## Archive Condition

Archive after implementation, verification, commit, and push.
