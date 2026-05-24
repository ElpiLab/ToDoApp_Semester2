# 580 Dashboard Refresh and ERD Sync

## Scope

Make the dashboard refresh dependency explicit and sync the architecture ERD artifacts to the actual SQLModel ORM metadata.

## Expected Files or Modules to Touch

- `src/student_task_manager/ui/dashboard_page.py`
- `src/student_task_manager/ui/routes.py`
- `docs/architecture/erd.drawio`
- `docs/architecture/erd.dbml`
- `docs/architecture/erd.png`
- relevant docs and prompt archive records

## Tests to Add or Update

- Existing dashboard behavior is covered through the default suite. Add focused tests only if the refactor changes callable behavior.

## Acceptance Criteria

- Dashboard quick-complete refresh does not recursively call `render_dashboard_page`.
- Dashboard refresh callback is explicit rather than optional.
- ERD source documents the real `student` and `task` tables, columns, defaults, nullability, indexes, foreign key, and enums from `models.py`.
- Any inconsistencies found are reported.
- Verification gates pass.

## Archive Condition

Archive after implementation, docs update, and successful verification.
