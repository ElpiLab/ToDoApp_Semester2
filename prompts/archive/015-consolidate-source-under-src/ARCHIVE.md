# 015 Consolidate Source Under src/ Archive

Date: 2026-05-20
Author: Codex
PR / Commit: N/A

Files changed:
- application.py
- pyproject.toml
- requirements.txt
- src/student_task_manager/data_access/*
- src/student_task_manager/domain/*
- src/student_task_manager/services/*
- src/student_task_manager/ui/*
- tests/test_task_service.py
- tests/test_task_controllers.py
- tests/conftest.py
- docs/Status.md
- docs/Roadmap.md
- docs/Changelog.md

Tests added/updated:
- tests/test_task_service.py
- tests/test_task_controllers.py

Commands run:
```bash
python -m pip install -e ".[dev]"
pytest tests/ --tb=short
ruff format --check src tests
ruff check src tests
python -m mypy src
python -c "import application; print('application import ok')"
```

Known risks and mitigations:
- Risk: The root `application.py` launcher is outside the package and outside the canonical Ruff command targets. Mitigation: it was formatted/linted directly during this change and import-checked after dependency refresh.
- Risk: `pytest` still reports a cache write warning for `C:/Users/lence/AppData/Local/ToDoApp_Semester2/pytest_cache`. Mitigation: the suite itself passed; cache permissions should be cleaned separately if the warning becomes noisy.

Follow-ups / rollback notes:
- Keep future Python source under `src/student_task_manager/`; do not reintroduce top-level `domain`, `services`, `data_access`, or `ui` packages.
- Authentication remains only partially aligned with user-scoped tasks; handle that under a separate prompt.
