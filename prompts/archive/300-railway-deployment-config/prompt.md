# 300 Railway Deployment Config

## Scope

Make the app start correctly on Railway while preserving the current local development default.

## Expected Files

- `application.py`
- `src/student_task_manager/deployment.py`
- `src/student_task_manager/data_access/db.py`
- `requirements.txt`
- `tests/`
- `README.md`
- `docs/Status.md`
- `docs/Changelog.md`

## Tests

- Add or update a focused test for deployment server configuration.
- Run the focused test plus formatting, lint, and mypy checks for touched code.

## Acceptance Criteria

- Local runs still default to `127.0.0.1:8081`.
- Railway runs can bind to `0.0.0.0:$PORT`.
- Invalid `PORT` values fail clearly.
- `DATABASE_URL` can be overridden for deployment storage.
- README includes concise Railway deployment steps and required variables.

## Archive Condition

Archive this prompt after code, docs, and verification are complete.
