# 020 Testing Requirements Alignment Archive

Date: 2026-05-20
Author: Codex
PR / Commit: N/A

Files changed:
- tests/test_task_service.py
- tests/test_task_dao.py
- tests/test_task_integration.py
- docs/TestCases.md
- docs/Status.md
- docs/Roadmap.md
- docs/Changelog.md

Tests added or updated:
- Updated service tests to keep the rubric unit-test count clear.
- Added 3 database tests in `tests/test_task_dao.py`.
- Added 3 integration tests in `tests/test_task_integration.py`.

Commands run:
```bash
pytest tests/ --tb=short
ruff format --check src tests
ruff check src tests
python -m mypy src
```

Known risks and mitigations:
- Risk: The project now has 13 automated tests because `tests/test_smoke.py` remains as an extra package smoke test. Mitigation: `docs/TestCases.md` explicitly maps the 12 rubric tests and notes that the smoke test is outside the rubric count.
- Risk: Authentication/user-scoped task behavior remains incomplete. Mitigation: The test-case documentation and planning docs record that as a follow-up instead of treating it as verified multi-user behavior.
- Risk: `pytest` still reports a cache write warning for `C:/Users/lence/AppData/Local/ToDoApp_Semester2/pytest_cache`. Mitigation: the suite itself passed; cache permissions can be addressed separately.

Follow-ups / rollback notes:
- Next prompt should address auth/user-scope cleanup so task ownership is explicit and testable.
