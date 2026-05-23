# 400 Extract Analytics Page

Date: 2026-05-24
Author: Codex
PR / Commit: N/A

Files changed:
- `src/student_task_manager/ui/analytics_page.py`
- `src/student_task_manager/ui/pages.py`
- `docs/Changelog.md`
- `docs/Roadmap.md`
- `docs/Status.md`
- `prompts/archive/400-extract-analytics-page/prompt.md`

Tests added/updated:
- N/A

Commands run:
```bash
python -m pip install -e ".[dev]"
pytest tests/test_ui_pages.py --tb=short
ruff format src tests
pytest tests/ --tb=short
ruff format --check src tests
ruff check src tests
python -m mypy src
```

Known risks & mitigations:
- Risk: Analytics charts could drift visually after extraction. Mitigation: the rendering code was moved behind a small wrapper, covered by the existing UI smoke tests, and should still be checked manually in the running app.

Follow-ups / rollback notes:
- Continue the page split with another low-risk page before attempting the larger Tasks or Calendar extraction.
