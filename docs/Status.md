# Status

This file records the current repository state.

## Current state

- Repository phase: active feature development
- Implementation state: the main pages are functional against SQLite:
  - **Dashboard page** (default landing) - stat cards (Total/Open/Completed/Overdue), Due today, Coming up (next 7 days), In progress, and High priority lists; all items click through to the task dialog.
  - **Tasks page** - Board view (default) and List view with drag-and-drop, Status/Priority/Sort filter dropdowns, global-header search, click-to-edit, confirmation-before-delete, styling matched to the Figma. CRUD round-trips end-to-end.
  - **Calendar page** - month grid with task pills, day-cell selection, side panel for the selected day, add-task button per day.
  - **Analytics page** - view-only task metrics and charts.
  - **Settings page** - profile fields and a task deletion action.
- Prompt workflow: templates and archived prompts exist through `130-polish-notification-bell`. Earlier UI work (Calendar page, Dashboard page, dialog redesign, sidebar cleanup) was iterative follow-up not driven by a numbered prompt.
- Planning docs: this file and `Changelog.md` are up to date as of 2026-05-20.
- Source layout: application code now lives under the installable `src/student_task_manager/` package. `application.py` remains at the repository root as the launcher.
- Test layout: the automated suite includes the required 12-test rubric mix documented in `docs/TestCases.md` (6 unit, 3 database, 3 integration), plus task-ownership regression tests and one package smoke test. Broader NiceGUI browser behavior is still exercised by hand.
- README: current and rubric-facing; it documents implemented behavior, source layout, ORM models, setup/run commands, test requirements, blank team-contribution rows, and future roadmap items.

## Active prompt

- N/A

## Next planned work

- **Login/profile polish** - refine authentication and profile behavior after user-scoped tasks are explicit.
- **UI module split** - reduce the size of the main NiceGUI page module when there is time.
- **Optional export/download** - add CSV/JSON export later if it becomes part of the submitted scope.

## Support boundary

- Tasks page is feature-complete for the current scope.
- `Dashboard`, `Tasks`, `Calendar`, `Analytics`, and `Settings` sidebar nav items are functional. `Modules` has been removed from the sidebar.
- Analytics is view-only for the current scope; CSV/JSON export is intentionally not exposed in the UI.

## Notes

- Use this file for current-state truth, not future planning.
- Tool caches are configured under `C:/Users/lence/AppData/Local/ToDoApp_Semester2/`.
