# 090 Clean Up Profile Save Validation

## Objective

Make the Settings profile save code easier to read and slightly stricter when validating email addresses.

## Scope

- Move profile-save imports from the nested function to module scope.
- Add a small email validation helper.
- Use the helper in `save_profile`.

## Expected Files To Touch

- `src/student_task_manager/ui/pages.py`
- `tests/test_ui_pages.py`

## Tests To Add Or Update

- Add focused tests for the email validation helper.

## Acceptance Criteria

- `save_profile` no longer contains inline imports.
- Email validation rejects empty/partial addresses such as `.@.`.
- Repository verification gates pass.

## Archive Condition

- Relevant tests and repository verification gates pass.
