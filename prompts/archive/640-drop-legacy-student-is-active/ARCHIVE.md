# Archive Summary

Date completed: 2026-05-24
Author: Codex
PR or commit SHA: N/A

## Files Changed

- `docs/Changelog.md`
- `docs/Roadmap.md`
- `src/student_task_manager/data_access/db.py`
- `tests/test_db_config.py`
- `prompts/archive/640-drop-legacy-student-is-active/ARCHIVE.md`
- `prompts/archive/640-drop-legacy-student-is-active/prompt.md`

## Tests Added or Updated

- `tests/test_db_config.py::test_migrate_legacy_student_is_active_drops_stale_not_null_column`
- `tests/test_db_config.py::test_migrate_legacy_student_is_active_is_idempotent`

## Commands Run

```bash
pytest tests/test_db_config.py --tb=short
python -m pip install -e ".[dev]"
pytest tests/ --tb=short
ruff format --check src tests
ruff check src tests
python -m mypy src
git diff --check
```

## Known Risks and Mitigations

- Risk: Existing Railway SQLite databases may have other stale columns from older development versions. Mitigation: this migration targets the confirmed blocking column from Railway logs and leaves unrelated data untouched.
- Risk: SQLite versions older than 3.35 do not support `ALTER TABLE ... DROP COLUMN`. Mitigation: local Python and Railway's Python 3.11 image are expected to use a modern SQLite; deployment logs will fail fast if the platform unexpectedly lacks support.

## Follow-ups or Rollback Notes

- After deployment, verify logs show `Dropping legacy student.is_active column` once, then register a fresh account.
