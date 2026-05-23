# 390 Extract Dashboard Page

## Scope

Extract the dashboard rendering code from `src/student_task_manager/ui/pages.py` into a focused dashboard module.

## Expected Files

- `src/student_task_manager/ui/pages.py`
- `src/student_task_manager/ui/dashboard_page.py`
- `docs/Changelog.md`
- `docs/Roadmap.md`
- `docs/Status.md`
- `prompts/archive/390-extract-dashboard-page/`

## Tests

- Keep existing UI helper tests passing.
- Run the focused UI test module and the full test suite.
- Run formatting, linting, and type checks.

## Acceptance Criteria

- `pages.py` delegates dashboard rendering to `dashboard_page.py`.
- Dashboard behavior remains unchanged: greeting, task summary cards, category progress, upcoming tasks, quick complete, and "View all tasks".
- Route setup, shared state, and page switching remain in `pages.py`.
- No task board, calendar, analytics, settings, authentication, or persistence behavior is changed.

## Archive Condition

Archive after the dashboard extraction is implemented, verified, and documented.
