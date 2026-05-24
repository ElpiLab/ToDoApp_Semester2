# Archive Summary

Date completed: 2026-05-24
Author: Codex
PR or commit SHA: 25bd81e

## Files Changed

- `README.md`
- `docs/Changelog.md`
- `docs/Roadmap.md`
- `src/student_task_manager/data_access/db.py`
- `tests/test_db_config.py`
- `prompts/archive/620-railway-volume-database-url/ARCHIVE.md`
- `prompts/archive/620-railway-volume-database-url/prompt.md`

## Tests Added or Updated

- `tests/test_db_config.py::test_database_url_defaults_to_railway_volume_when_deployed`
- `tests/test_db_config.py::test_database_url_corrects_legacy_railway_absolute_data_path`
- `tests/test_db_config.py::test_database_url_respects_explicit_non_legacy_railway_database_url`

## Commands Run

```bash
pytest tests/test_db_config.py tests/test_browser_smoke.py tests/test_auth_service.py --tb=short
python -m pip install -e ".[dev]"
pytest tests/ --tb=short
ruff format --check src tests
ruff check src tests
python -m mypy src
git diff --check
```

## Known Risks and Mitigations

- Risk: Existing accounts previously written to an ephemeral or wrong SQLite path will not automatically appear in the persistent volume database. Mitigation: new Railway deployments now use `/app/data/todo.db`; if the old file is still accessible, it must be manually copied into the volume.
- Risk: Explicit Railway `DATABASE_URL` values other than the known bad `/data/todo.db` path are still respected. Mitigation: this keeps custom deployments working while correcting the observed misconfiguration.

## Follow-ups or Rollback Notes

- After deployment, register with a fresh email and verify the account survives a Railway redeploy or restart.
