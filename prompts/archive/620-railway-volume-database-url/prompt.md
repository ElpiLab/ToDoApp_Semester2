# 620 Railway Volume Database URL

## Scope

Make Railway deployments use the persistent `/app/data` volume for SQLite by default and guard against the known bad `/data/todo.db` path.

## Expected Files or Modules to Touch

- `src/student_task_manager/data_access/db.py`
- `tests/test_db_config.py`
- `README.md`
- relevant docs and prompt archive records

## Tests to Add or Update

- Add database URL tests for Railway default behavior.
- Add database URL tests for correcting the legacy `/data/todo.db` Railway path.

## Acceptance Criteria

- Local default remains `sqlite:///data/todo.db`.
- Railway default becomes `sqlite:////app/data/todo.db`.
- Railway `DATABASE_URL=sqlite:////data/todo.db` is corrected to `sqlite:////app/data/todo.db`.
- Explicit non-legacy `DATABASE_URL` values remain supported.
- Verification gates pass.

## Archive Condition

Archive after implementation, verification, commit, and push.
