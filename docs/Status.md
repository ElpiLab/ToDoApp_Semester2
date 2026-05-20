# Status

This file records the current repository state.

## Current state

- Repository phase: active feature development
- Implementation state: three pages are functional against SQLite:
  - **Tasks page** - Board view (default) and List view with drag-and-drop, Status/Priority/Sort filter dropdowns, global-header search, click-to-edit, confirmation-before-delete, styling matched to the Figma. CRUD round-trips end-to-end.
  - **Calendar page** - month grid with task pills, day-cell selection, side panel for the selected day, add-task button per day.
  - **Dashboard page** (default landing) - stat cards (Total/Open/Completed/Overdue), Due today, Coming up (next 7 days), In progress, and High priority lists; all items click through to the task dialog.
- Prompt workflow: templates and the archived `010-task-list-view-foundation` and `015-consolidate-source-under-src` prompts exist. Recent UI work (Calendar page, Dashboard page, dialog redesign, sidebar cleanup) was iterative follow-up not driven by a numbered prompt.
- Planning docs: this file and `Changelog.md` are up to date as of 2026-05-20.
- Source layout: application code now lives under the installable `src/student_task_manager/` package. `application.py` remains at the repository root as the launcher.
- Test layout: service and controller regression coverage exists; broader UI behavior is exercised by hand.

## Active prompt

- N/A

## Next planned work

- **Analytics page** - replace the placeholder sidebar entry with a real view (charts/summary metrics over tasks). No numbered prompt yet.
- **Login page** - introduce authentication and a user-scoped task model. No numbered prompt yet; will need a domain decision on User/Student before implementation.
- **Settings page** (`040-settings-preferences-and-polish`) - user preferences, polish, and lower-priority cleanup after the core flows are landed.

## Support boundary

- Tasks page is feature-complete for the current scope.
- `Dashboard` and `Calendar` sidebar nav items are functional. `Modules` has been removed from the sidebar. `Analytics` and `Settings` are still visual placeholders; clicking them does nothing yet.
- Notification bell + settings gear in the global header are visual placeholders.
- The user chip in the sidebar shows a hardcoded "Alex C." - pending a Student/Profile decision.

## Notes

- Use this file for current-state truth, not future planning.
- Tool caches are configured under `C:/Users/lence/AppData/Local/ToDoApp_Semester2/`.
