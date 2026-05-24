# 640 Drop Legacy Student Is Active

## Scope

Fix Railway registration against persistent databases that still contain the removed `student.is_active` column.

## Expected Files or Modules to Touch

- `src/student_task_manager/data_access/db.py`
- `tests/test_db_config.py`
- docs and prompt archive records

## Tests to Add or Update

- Add a database migration regression test proving a legacy `student.is_active NOT NULL` column is removed before new registrations need to insert students.

## Acceptance Criteria

- `Student` model does not reintroduce `is_active`.
- Startup migration drops stale `student.is_active` when present.
- The migration is idempotent when the column is already absent.
- Relevant tests and verification gates pass.

## Archive Condition

Archive after the fix is committed and pushed to `main`.
