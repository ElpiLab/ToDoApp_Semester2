# 550 Review Hardening Follow-ups

## Scope

Implement the review findings from the repository bug, invariant, consistency, and security pass.

## Expected Files or Modules to Touch

- `src/student_task_manager/services/auth_service.py`
- `src/student_task_manager/services/task_service.py`
- `src/student_task_manager/deployment.py`
- `src/student_task_manager/ui/settings_page.py` only if UI/server validation needs alignment
- `src/student_task_manager/ui/view_helpers.py`
- `tests/test_auth_service.py`
- `tests/test_task_service.py`
- `tests/test_application.py`
- `tests/test_ui_pages.py`
- `docs/architecture/erd.dbml`
- `docs/architecture/erd.drawio`
- `docs/architecture/erd.png` if practical with available tooling
- `AGENTS.md`
- `.github/instructions/python.instructions.md`
- relevant status, roadmap, changelog, or test-case docs when behavior or workflow changes

## Tests to Add or Update

- Regression tests for invalid task enum update values.
- Regression tests for profile validation in `AuthService`.
- Regression tests for password byte-length limits.
- Regression tests for public-host storage secret enforcement.
- Regression tests for corrected due-date display text.

## Acceptance Criteria

- Task updates reject invalid `Priority` and `Status` values before DAO writes.
- Auth profile updates validate name and email in the service layer.
- Password creation and password changes reject passwords over bcrypt's 72-byte input limit with an actionable error.
- Public host deployment config cannot fall back to the development storage secret.
- ERD source matches the current SQLModel entities and fields.
- Mojibake in user-visible due-date helper text is removed.
- Agent verification guidance is consistent across repo instructions.
- Relevant tests and quality gates pass or any unavailable gate is explicitly reported.

## Archive Condition

Archive this prompt after the implementation is complete, docs are updated, and the relevant verification commands have passed.
