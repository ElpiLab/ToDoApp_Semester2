# Prompt 530 Archive: Fix Pytest Cache Warning

## Date Completed

2026-05-24

## Author

Codex

## PR or Commit SHA

N/A

## Files Changed

- `pyproject.toml`
- `AGENTS.md`
- `docs/Status.md`
- `docs/Roadmap.md`
- `docs/Changelog.md`

## Tests Added or Updated

N/A

## Commands Run

```bash
python -m pip install -e ".[dev]"
pytest tests/ --tb=short
ruff format --check src tests
ruff check src tests
python -m mypy src
```

## Known Risks and Mitigations

- Pytest no longer stores cache metadata such as node IDs and last-failed tests. This trades a small convenience feature for warning-free, deterministic sandboxed verification.

## Follow-ups or Rollback Notes

- If the Windows cache ACL issue is resolved later, the pytest cache provider can be re-enabled by removing `-p no:cacheprovider` from `pyproject.toml`.
