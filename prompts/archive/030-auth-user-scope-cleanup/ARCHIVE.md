# 030 Auth User Scope Cleanup Archive

Date: 2026-05-20
Author: Codex
PR / Commit: N/A

Files changed:
- src/student_task_manager/data_access/dao.py
- src/student_task_manager/services/task_service.py
- src/student_task_manager/ui/controllers.py
- tests/test_task_service.py
- tests/test_task_controllers.py
- tests/test_task_dao.py
- tests/test_task_integration.py
- docs/TestCases.md
- docs/Status.md
- docs/Roadmap.md
- docs/Changelog.md

Tests added or updated:
- Updated task service, controller, DAO, and integration tests to pass explicit user IDs.
- Added service, DAO, controller, and integration regression tests for task ownership isolation.

Commands run:
```bash
pytest tests/ --tb=short
ruff format --check src tests
ruff check src tests
python -m mypy src
```

Known risks and mitigations:
- Risk: NiceGUI browser behavior was not automated in this prompt. Mitigation: controller and service boundaries are covered, and broader browser behavior remains a documented manual-test area.
- Risk: `pytest` still reports a cache write warning for `C:/Users/lence/AppData/Local/ToDoApp_Semester2/pytest_cache`. Mitigation: the suite itself passed; cache permissions can be addressed separately.

Follow-ups / rollback notes:
- Review login/registration polish and README accuracy in a separate prompt.
- If rolling back, restore the previous service/controller signatures together; mixed signatures will break task actions.
