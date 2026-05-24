# 460 Extract Notification Menu

Date: 2026-05-24
Author: Codex
PR / Commit: N/A

Files changed:
- `src/student_task_manager/ui/pages.py`
- `src/student_task_manager/ui/notifications.py`
- `docs/Changelog.md`
- `docs/Roadmap.md`
- `docs/Status.md`
- `prompts/archive/460-extract-notification-menu/prompt.md`
- `prompts/archive/460-extract-notification-menu/ARCHIVE.md`

Tests added/updated:
- N/A

Commands run:
```bash
python -m mypy src\student_task_manager\ui\pages.py src\student_task_manager\ui\notifications.py
pytest tests\test_ui_pages.py --tb=short
ruff format --check src\student_task_manager\ui\pages.py src\student_task_manager\ui\notifications.py
ruff format src\student_task_manager\ui\pages.py src\student_task_manager\ui\notifications.py
ruff check src\student_task_manager\ui\pages.py src\student_task_manager\ui\notifications.py
```

Known risks and mitigations:
- Risk: notification read-state behavior could drift during extraction. Mitigation: manual smoke test verified bell dot, notification menu, click-to-open, and read-state behavior.

Follow-ups / rollback notes:
- If a regression appears, move notification rendering back into `pages.py` or keep `NotificationMenu` but narrow its API around the broken callback.
