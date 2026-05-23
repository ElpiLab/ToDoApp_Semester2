# 370 Final Rubric Doc And Due Date Cleanup

Date: 2026-05-23
Author: Codex
PR / Commit: N/A

Files changed:
- `src/student_task_manager/ui/pages.py`
- `README.md`
- `docs/Roadmap.md`
- `docs/Changelog.md`
- `prompts/archive/370-final-rubric-doc-and-due-date-cleanup/prompt.md`
- `prompts/archive/370-final-rubric-doc-and-due-date-cleanup/ARCHIVE.md`

Tests added/updated:
- N/A

Commands run:
```bash
pytest tests/test_ui_pages.py --tb=short
pytest tests/ --tb=short
ruff format src/student_task_manager/ui/pages.py
ruff format --check src tests
ruff check src tests
python -m mypy src
```

Known risks & mitigations:
- Risk: new tasks without due dates now appear as unscheduled instead of due today. Mitigation: this matches the README and keeps due dates intentionally optional.

Follow-ups / rollback notes:
- If the team decides every task must require a due date, restore the previous default or add explicit form validation instead.
