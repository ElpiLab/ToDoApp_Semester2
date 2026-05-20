# 060 Fix Windows App Startup

Date: 2026-05-20
Author: Codex
PR / Commit: 81d6e0a

Files changed:
- application.py
- src/student_task_manager/data_access/db.py
- docs/Status.md
- docs/Roadmap.md
- docs/Changelog.md

Tests added/updated:
- N/A

Commands run:
```bash
python -c "from application import create_db_and_tables, create_default_user; create_db_and_tables(); create_default_user(); print('startup bootstrap ok')"
python -m pip install -e ".[dev]"
pytest tests/ --tb=short
ruff format --check src tests
ruff check src tests
python -m mypy src
```

Known risks and mitigations:
- Risk: full background server probing in the sandbox hit a Windows process-pool permission error after NiceGUI reported the local URL. Mitigation: the actual startup crash from console encoding is fixed, and the user should run the app directly in their normal PowerShell terminal.

Follow-ups / rollback notes:
- If SQL query logging is needed for debugging, temporarily set `echo=True` locally in `src/student_task_manager/data_access/db.py`.
