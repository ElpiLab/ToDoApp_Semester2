# 630 Registration Diagnostics

## Scope

Add minimal server-side diagnostics for Railway registration failures without exposing passwords or changing the public registration contract.

## Expected Files or Modules to Touch

- `application.py`
- `src/student_task_manager/data_access/db.py`
- `src/student_task_manager/services/auth_service.py`
- targeted tests for logging/helper behavior

## Tests to Add or Update

- Unit coverage for safe database URL logging.
- Unit coverage that duplicate registration logs the duplicate path.

## Acceptance Criteria

- Startup logs show the effective database URL with credentials hidden.
- Registration logs distinguish an existing email from an unexpected database integrity failure.
- UI still shows the existing generic duplicate-registration message.
- Existing verification gates pass.

## Archive Condition

Archive after implementation is committed and pushed or after the user explicitly decides not to keep the diagnostics.
