# ARCHIVE.md - Prompt archive summary

Date: 2026-05-24
Author: Codex
PR / Commit: N/A

Files changed:
- src/student_task_manager/ui/pages.py
- src/student_task_manager/ui/tasks_page.py
- docs/Changelog.md
- docs/Roadmap.md
- docs/Status.md
- prompts/archive/450-extract-task-controls/prompt.md
- prompts/archive/450-extract-task-controls/ARCHIVE.md

Tests added/updated:
- N/A

Commands run (copyable):
```bash
python -m mypy src\student_task_manager\ui\pages.py src\student_task_manager\ui\tasks_page.py
pytest tests\test_ui_pages.py --tb=short
ruff check src\student_task_manager\ui\pages.py src\student_task_manager\ui\tasks_page.py
ruff format --check src\student_task_manager\ui\pages.py src\student_task_manager\ui\tasks_page.py
python -m pip install -e ".[dev]"
pytest tests/ --tb=short
ruff format --check src tests
ruff check src tests
python -m mypy src
```

Known risks & mitigations:
- Risk: task filter/search/toggle callbacks were moved out of `pages.py`, so event wiring could regress. Mitigation: focused UI page tests passed, full suite passed, and manual Tasks smoke testing confirmed the controls still work.
- Risk: prompt archive was created before the final commit SHA existed. Mitigation: commit SHA can be read from Git history after commit.

Follow-ups / rollback notes:
- Continue reducing `pages.py` only with small prompt-driven extractions.
- Roll back by reverting the eventual commit for this archive if the extracted controls regress.
