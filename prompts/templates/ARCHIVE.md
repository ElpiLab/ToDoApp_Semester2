# ARCHIVE.md — Prompt archive summary (template)

Date: YYYY-MM-DD
Author: Your Name <you@example.com>
PR / Commit: <url-or-sha>

Files changed:
- src/path/to/file.py
- tests/unit/test_example.py

Tests added/updated:
- tests/unit/test_example.py

Commands run (copyable):
```bash
python -m pip install -e ".[dev]"
pytest tests/ --tb=short
ruff format --check src tests
ruff check src tests
python -m mypy src
```

Known risks & mitigations:
- Risk: explanation of risk. Mitigation: what to watch for / rollback steps.

Follow-ups / rollback notes:
- Optional follow-up tasks or instructions to revert if needed.

Notes:
- Keep this summary short and factual. Do not edit the original prompt file.
- If a field does not apply or has no value yet, write `N/A`.
