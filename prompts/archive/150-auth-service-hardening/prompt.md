# 150 Auth Service Hardening

## Scope

- Remove the unused broken `AuthService.register` method.
- Enforce password-change validation in `AuthService.change_password`.
- Leave registration UI refactoring as a follow-up.

## Expected files or modules to touch

- `src/student_task_manager/services/auth_service.py`
- `tests/test_auth_service.py`
- prompt archive files for this prompt

## Tests to add or update

- Add regression coverage for rejecting too-short replacement passwords.
- Add regression coverage for rejecting reuse of the current password.

## Acceptance criteria

- `AuthService.register` is no longer present.
- `change_password` rejects weak new passwords before writing a new hash.
- `change_password` rejects a new password that matches the verified current password.
- Existing auth and task tests continue to pass.

## Archive condition

- Archive this prompt after the implementation is complete and relevant verification passes.

## Follow-up

- Move `/register` persistence logic behind `AuthService` after upload timing risk is lower.
