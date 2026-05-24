# ARCHIVE.md - Prompt archive summary

Date: 2026-05-24
Author: Codex
PR / Commit: N/A

Files changed:
- src/student_task_manager/ui/pages.py
- src/student_task_manager/ui/calendar_page.py
- docs/Changelog.md
- docs/Roadmap.md
- docs/Status.md
- prompts/archive/420-extract-calendar-page/prompt.md
- prompts/archive/420-extract-calendar-page/ARCHIVE.md

Tests added/updated:
- N/A

Commands run (copyable):
```bash
ruff format src tests
pytest tests/test_ui_pages.py --tb=short
python -m pip install -e ".[dev]"
pytest tests/ --tb=short
ruff format --check src tests
ruff check src tests
python -m mypy src
```

Known risks & mitigations:
- Risk: Calendar behavior could drift during extraction. Mitigation: renderer delegates all state changes back through the existing callbacks, and the focused UI page tests plus full verification gates passed.

Follow-ups / rollback notes:
- Continue the UI module split with the Tasks page and route shell when time allows.
- Roll back by moving `render_calendar_page` back into `pages.py` and restoring the removed imports.
