# Roadmap

This file tracks planned work and execution order.

## Active sequence

1. **Login/profile polish** (no numbered prompt yet)
   Clean up authentication documentation and any remaining login/registration behavior after user-scoped tasks are explicit.
2. **UI module split** (no numbered prompt yet)
   Continue breaking down the large NiceGUI page module into smaller page modules. The pure helper functions and dashboard renderer have already been extracted.
3. **Optional export/download** (future scope)
   Add CSV/JSON task export later if it becomes useful for the final submission.
4. **Persisted user preferences** (future scope)
   Add storage for default landing page, default task view, default priority, notification toggles, and appearance theme. These controls are not shown in the current Settings page because they are not persisted yet.

## Archived prompts

- `000-bootstrap-project-scaffold`
  Bootstrap scaffold, planning docs, shared agent instructions, package skeleton, and default verification setup.
- `010-task-list-view-foundation`
  Replaced the raw NiceGUI scaffold with the first structured task-list screen and improved task-flow verification.
- `015-consolidate-source-under-src`
  Moved the active application packages under `src/student_task_manager/` and made the default verification gates check the real source package.
- `020-testing-requirements-alignment`
  Added the required 12-test mix and documented the test cases in the course template format.
- `030-auth-user-scope-cleanup`
  Scoped task operations to the authenticated user and added ownership regression tests.
- `040-readme-rubric-documentation-cleanup`
  Rewrote the README to match the current app, architecture, ORM model, run commands, and testing rubric.
- `050-readme-contributions-and-export-scope`
  Added README contribution and future-roadmap sections, and kept export/download out of the current UI scope.
- `060-fix-windows-app-startup`
  Fixed Windows console startup output and disabled noisy SQLAlchemy echo logging.
- `070-narrow-controller-error-handling`
  Kept validation errors user-facing while letting unexpected controller errors surface.
- `080-clarify-temporary-settings-controls`
  Clarified temporary Settings controls before they were removed from the current scope.
- `090-clean-up-profile-save-validation`
  Tightened Settings profile email validation and made profile-save imports explicit.
- `100-polish-app-ui-wording-and-navigation`
  Polished app wording and moved profile/settings controls into clearer locations.
- `110-clarify-settings-preview-controls`
  Reworded temporary Settings controls before the Settings page was simplified.
- `120-simplify-settings-page`
  Removed non-persisting Settings cards and documented persisted preferences as future scope.
- `130-polish-notification-bell`
  Kept the notification bell as an unread dot and added session-level read actions to the notification menu.
- `140-dashboard-progress-card`
  Changed the dashboard completed-task card into a percentage-based progress card.
- `150-auth-service-hardening`
  Hardened password-change validation and removed unused broken registration service code.
- `160-calendar-sidebar-priority-colors`
  Fixed calendar sidebar task accents so upcoming tasks use priority colors and overdue tasks stay red.
- `170-calendar-sidebar-clear-label`
  Reworked the calendar sidebar clear action into more helpful upcoming-task wording.
- `180-calendar-sidebar-clear-label-specificity`
  Made calendar sidebar clear labels more specific to the selected-day state.
- `190-calendar-upcoming-header-label`
  Clarified the calendar upcoming sidebar header label.
- `200-calendar-sidebar-back-label`
  Added a clearer back label when switching from selected-day tasks to upcoming tasks.
- `210-calendar-empty-day-clear-label`
  Improved empty-day calendar sidebar wording.
- `220-move-task-search-to-toolbar`
  Moved task search from the global header into the Tasks toolbar.
- `230-task-toolbar-button-consistency`
  Polished task toolbar button and view-control consistency.
- `240-polish-task-toolbar-controls`
  Improved task toolbar filter sizing, wrapping, and search wording.
- `250-move-task-view-switch`
  Moved the Board/List switch beside the page heading.
- `260-task-view-toggle-active-background`
  Added a visible active background to the task view toggle.
- `270-task-view-toggle-selected-segment`
  Strengthened the selected Board/List segment styling.
- `280-task-view-toggle-inactive-white`
  Kept inactive Board/List segments white.
- `290-remove-misleading-sort-control`
  Removed the misleading Sort by dropdown from Tasks.
- `300-railway-deployment-config`
  Prepared the app for Railway deployment with port, host, database URL, and secret configuration.
- `310-remove-tracked-nicegui-storage`
  Removed tracked NiceGUI runtime storage from source control.
- `320-status-label-consistency`
  Changed remaining Open labels to To do where they represented pending tasks.
- `330-task-status-filter-consistency`
  Aligned task status filter wording with To do / In Progress / Done.
- `340-list-badge-alignment`
  Aligned List view priority and status badges with stable right-side columns.
- `360-fix-task-category-other-option`
  Restored Other as a task category option.
- `370-final-rubric-doc-and-due-date-cleanup`
  Kept new task due dates optional by default, synced archived prompt records, and clarified team contributions.
- `380-extract-ui-view-helpers`
  Extracted pure UI helper constants and formatting/filter functions from the main NiceGUI page module.
- `390-extract-dashboard-page`
  Extracted dashboard rendering from the main NiceGUI page module into a focused dashboard module.

## Notes

- The roadmap is sequencing, not a status ledger.
- Update this file when prompt order or planned work changes.
