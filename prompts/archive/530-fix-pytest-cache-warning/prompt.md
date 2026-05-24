# 530 Fix Pytest Cache Warning

## Scope

Remove the pytest cache warning seen during verification by making the configured test cache path writable and aligned with repo hygiene.

## Expected Files or Modules to Touch

- `pyproject.toml`
- `AGENTS.md`
- `docs/Changelog.md`
- relevant prompt archive files

## Tests to Add or Update

- No application tests are expected; verify with the standard pytest command and lint/type gates.

## Acceptance Criteria

- `pytest tests/ --tb=short` completes without `PytestCacheWarning`.
- Repo documentation accurately describes where tool caches live.
- The standard verification gates remain green.

## Archive Condition

Archive after verification passes without the cache warning.
