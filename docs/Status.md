# Status

This file records the current repository state.

## Current state

- Repository phase: active feature development
- Implementation state: the main pages are functional against SQLite:
  - **Dashboard page** (default landing) - stat cards (Active/Progress/Overdue), Due today, Coming up (next 7 days), In Progress, and High priority lists; all items click through to the task dialog.
  - **Tasks page** - Board view (default) and List view with drag-and-drop, To do / In Progress / Done status filtering, Priority/Category filter dropdowns, task-toolbar search, click-to-edit, confirmation-before-delete, styling matched to the Figma, and consistent To do / In Progress / Done status labels. CRUD round-trips end-to-end.
  - **Calendar page** - month grid with task pills, day-cell selection, side panel for the selected day, add-task button per day.
  - **Analytics page** - view-only task metrics and charts.
  - **Settings page** - profile fields and a task deletion action.
- Prompt workflow: templates and archived prompts exist through `590-collapse-task-status-states`. Earlier UI work (dialog redesign, sidebar cleanup) was iterative follow-up not driven by a numbered prompt.
- Planning docs: this file and `Changelog.md` are up to date as of 2026-05-24.
- Source layout: application code now lives under the installable `src/student_task_manager/` package. `application.py` remains at the repository root as the launcher and explicitly registers NiceGUI routes before startup. NiceGUI route orchestration lives in `src/student_task_manager/ui/routes.py`. Pure UI formatting/filter helpers live in `src/student_task_manager/ui/view_helpers.py`; dashboard rendering lives in `src/student_task_manager/ui/dashboard_page.py`; analytics rendering lives in `src/student_task_manager/ui/analytics_page.py`; settings rendering lives in `src/student_task_manager/ui/settings_page.py`; calendar rendering lives in `src/student_task_manager/ui/calendar_page.py`; task create/edit dialog rendering lives in `src/student_task_manager/ui/task_dialog.py`; task board/list rendering and task header/search/filter controls live in `src/student_task_manager/ui/tasks_page.py`; notification menu rendering and read-state helpers live in `src/student_task_manager/ui/notifications.py`; shared sidebar, header, navigation, and profile-menu rendering live in `src/student_task_manager/ui/app_shell.py`.
- Deployment: Railway config is present; the launcher reads Railway's `PORT`, binds deployed runs to `0.0.0.0`, requires `STORAGE_SECRET` for deployed runs, and supports a `DATABASE_URL` override for persistent storage. Local SQLite defaults to `sqlite:///data/todo.db`. Production uses a Railway volume mounted at `/app/data` with `DATABASE_URL=sqlite:////app/data/todo.db`. `runtime.txt` pins the Nixpacks Python runtime to `python-3.11.9`, matching the project tooling target.
- Test layout: the automated suite includes the required 12-test rubric mix documented in `docs/TestCases.md` (6 unit, 3 database, 3 integration), plus task-ownership, validation, deployment-secret, UI-helper, package-smoke, and NiceGUI simulated-browser smoke tests. Broader full-browser behavior is still exercised by hand.
- README: current and rubric-facing; it documents implemented behavior, selected wireframes, source layout, ORM models, setup/run commands, local DB reset expectations, Railway persistence, test requirements, team contributions, and links to the roadmap for future scope.
- Architecture ERD artifacts live under `docs/architecture/` and match the current SQLModel ORM metadata for the `student` and `task` tables, including defaults, nullability, indexes, the foreign key, and enum value sets.

## Active prompt

- N/A

## Support boundary

- Tasks page is feature-complete for the current scope.
- `Dashboard`, `Tasks`, `Calendar`, `Analytics`, and `Settings` sidebar nav items are functional. `Modules` has been removed from the sidebar.
- Analytics is view-only for the current scope; CSV/JSON export is intentionally not exposed in the UI.

## Notes

- Use this file for current-state truth, not future planning.
- Tool caches are configured under `C:/Users/lence/AppData/Local/ToDoApp_Semester2/`.
- Auth is suitable for the course project scope, not a full production identity system. Current safeguards include in-memory login throttling, generic registration failures for duplicate emails, current-password re-authentication for email changes, and explicit bcrypt input limits. Known limitations: no persistent/distributed throttling and no account recovery flow.
- Passwords must be at least 10 characters and fit bcrypt's 72-byte input limit; registration and password changes reject values outside that range explicitly.
- Task statuses are `pending`, `in_progress`, and `done`; the UI labels `pending` as To do. Startup database bootstrap migrates legacy `created` task rows to `pending`.
- Known UI limitation: the task dialog's "Add another" checkbox does not keep the dialog open when creating a task from Board/Kanban add-task entry points.
