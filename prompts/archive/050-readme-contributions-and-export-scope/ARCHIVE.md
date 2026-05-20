# 050 README Contributions and Export Scope

Date: 2026-05-20
Author: Codex
PR / Commit: 6f02726

Files changed:
- README.md
- src/student_task_manager/ui/pages.py
- docs/Status.md
- docs/Roadmap.md
- docs/Changelog.md

Tests added/updated:
- N/A

Commands run:
```bash
python -m pip install -e ".[dev]"
pytest tests/ --tb=short
ruff format --check src tests
ruff check src tests
python -m mypy src
```

Known risks and mitigations:
- Risk: export/download might be expected later. Mitigation: it is documented as future scope in the README and roadmap.

Follow-ups / rollback notes:
- Reintroduce CSV/JSON export behind a separate prompt if it becomes part of the final submission scope.
