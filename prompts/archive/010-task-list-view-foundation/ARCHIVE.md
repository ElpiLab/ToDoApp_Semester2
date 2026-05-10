# ARCHIVE.md

Date: 2026-05-09
Author: Codex <N/A>
PR / Commit: N/A

Files changed:
- application.py
- pyproject.toml
- src/student_task_manager/__init__.py
- ui/controllers.py
- ui/pages.py
- services/task_service.py
- data_access/dao.py
- docs/Roadmap.md
- docs/Status.md
- docs/Changelog.md
- tests/test_task_service.py
- tests/test_task_controllers.py

Tests added/updated:
- tests/test_task_service.py
- tests/test_task_controllers.py
- tests/test_smoke.py

Commands run (copyable):
```bash
python -m pytest tests --tb=short
python -m ruff format application.py domain data_access services ui tests
python -m ruff format --check application.py domain data_access services ui tests
python -m ruff check application.py domain data_access services ui tests
python -m mypy --explicit-package-bases application.py domain data_access services ui tests
```

Known risks & mitigations:
- Risk: the repository still mixes top-level implementation modules with a partially separate `src/` package layout. Mitigation: address the packaging/layout cleanup in a follow-up prompt before the codebase grows much further.
- Risk: NiceGUI screen behavior is covered mainly through service and controller regression tests, not end-to-end browser tests. Mitigation: add browser-level verification when the UI surface stabilizes further.

Follow-ups / rollback notes:
- Create the next prompt for dashboard and summary-query work only after the task-list flow remains stable under further changes.
- If rollback is needed, revert the archived prompt's file set together rather than selectively restoring the old scaffold page.
