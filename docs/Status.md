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
- Prompt workflow: templates and archived prompts exist through `400-extract-analytics-page`. Earlier UI work (Calendar page, Dashboard page, dialog redesign, sidebar cleanup) was iterative follow-up not driven by a numbered prompt.
- Planning docs: this file and `Changelog.md` are up to date as of 2026-05-24.
- Source layout: application code now lives under the installable `src/student_task_manager/` package. `application.py` remains at the repository root as the launcher. Pure UI formatting/filter helpers live in `src/student_task_manager/ui/view_helpers.py`; dashboard rendering lives in `src/student_task_manager/ui/dashboard_page.py`; analytics rendering lives in `src/student_task_manager/ui/analytics_page.py`; the remaining page-level UI split is follow-up work.
- Deployment: Railway config is present; the launcher reads Railway's `PORT`, binds deployed runs to `0.0.0.0`, and supports a `DATABASE_URL` override for persistent storage. Production uses a Railway volume mounted at `/app/data` with `DATABASE_URL=sqlite:////app/data/todo.db`.
- Test layout: the automated suite includes the required 12-test rubric mix documented in `docs/TestCases.md` (6 unit, 3 database, 3 integration), plus task-ownership regression tests and one package smoke test. Broader NiceGUI browser behavior is still exercised by hand.
- README: current and rubric-facing; it documents implemented behavior, selected wireframes, source layout, ORM models, setup/run commands, Railway persistence, test requirements, blank team-contribution rows, and future roadmap items.

## Active prompt

- N/A

## Next planned work

- **Login/profile polish** - refine authentication and profile behavior after user-scoped tasks are explicit.
- **Registration service boundary cleanup** - move `/register` persistence and validation behind `AuthService` after upload timing risk is lower.
- **UI module split** - continue reducing the main NiceGUI page module by extracting page renderers and shared components when there is time.
- **Optional export/download** - add CSV/JSON export later if it becomes part of the submitted scope.

## Support boundary

- Tasks page is feature-complete for the current scope.
- `Dashboard`, `Tasks`, `Calendar`, `Analytics`, and `Settings` sidebar nav items are functional. `Modules` has been removed from the sidebar.
- Analytics is view-only for the current scope; CSV/JSON export is intentionally not exposed in the UI.

## Notes

- Use this file for current-state truth, not future planning.
- Tool caches are configured under `C:/Users/lence/AppData/Local/ToDoApp_Semester2/`.
