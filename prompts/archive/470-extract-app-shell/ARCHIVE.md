# 470 Extract App Shell Archive

## Date Completed

2026-05-24

## Author

Codex

## PR or Commit SHA

N/A

## Files Changed

- `src/student_task_manager/ui/pages.py`
- `src/student_task_manager/ui/app_shell.py`
- `docs/Changelog.md`
- `docs/Roadmap.md`
- `docs/Status.md`
- `prompts/archive/470-extract-app-shell/prompt.md`
- `prompts/archive/470-extract-app-shell/ARCHIVE.md`

## Tests Added or Updated

N/A

## Commands Run

- `python -m mypy src\student_task_manager\ui\pages.py src\student_task_manager\ui\app_shell.py`
- `pytest tests\test_ui_pages.py --tb=short`
- `ruff check src\student_task_manager\ui\pages.py src\student_task_manager\ui\app_shell.py`
- `ruff format --check src\student_task_manager\ui\pages.py src\student_task_manager\ui\app_shell.py`

## Manual Verification

- User confirmed sidebar navigation, header actions, notification menu, settings shortcut, profile menu, and task dialog behavior still work locally.

## Known Risks and Mitigations

- Risk: this extraction moved shared layout code that every page depends on.
- Mitigation: focused UI tests, mypy, ruff, local startup, and manual smoke testing passed.

## Follow-ups or Rollback Notes

- Continue the UI module split only in small, verified phases.
