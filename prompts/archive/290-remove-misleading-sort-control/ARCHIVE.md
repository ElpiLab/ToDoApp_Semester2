# Archive Summary

Date: 2026-05-23
Author: Codex
PR / Commit: N/A

Files changed:
- `src/student_task_manager/ui/pages.py`
- `docs/Status.md`
- `docs/Changelog.md`
- `prompts/archive/290-remove-misleading-sort-control/prompt.md`
- `prompts/archive/290-remove-misleading-sort-control/ARCHIVE.md`

Tests added/updated:
- N/A

Commands run:
```bash
pytest tests/test_ui_pages.py --tb=short
ruff format src/student_task_manager/ui/pages.py
ruff format --check src/student_task_manager/ui/pages.py
ruff check src/student_task_manager/ui/pages.py
```

Known risks & mitigations:
- Risk: Board view no longer receives a pre-sorted task list from the removed global sort branch. Mitigation: Board columns and List sections both keep their own explicit due-date ordering where the UI depends on it.

Follow-ups / rollback notes:
- Reintroduce sorting only if it is designed as a clear per-view feature and tested against both Board and List behavior.
