# Roadmap

This file tracks planned work and execution order.

## Active sequence

1. **UI component cleanup** (future scope)
   The large NiceGUI route module has been split into focused route, page, shell, dialog, notification, and helper modules. Optional follow-up work can extract smaller repeated components if that improves readability.
2. **Optional export/download** (future scope)
   Add CSV/JSON task export later if it becomes useful for the final submission.
3. **Persisted user preferences** (future scope)
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
- `400-extract-analytics-page`
  Extract analytics rendering from the main NiceGUI page module into a focused analytics module.
- `410-extract-settings-page`
  Extract settings rendering from the main NiceGUI page module into a focused settings module.
- `420-extract-calendar-page`
  Extract calendar rendering from the main NiceGUI page module into a focused calendar module.
- `430-extract-task-dialog`
  Extract task create/edit dialog rendering from the main NiceGUI page module into a focused dialog module.
- `440-extract-tasks-page`
  Extract task board/list rendering from the main NiceGUI page module into a focused tasks module.
- `450-extract-task-controls`
  Extract task header, search, filters, and Board/List toggle rendering from the main NiceGUI page module into the focused tasks module.
- `460-extract-notification-menu`
  Extract notification menu rendering and read-state helpers from the main NiceGUI page module into a focused notification module.
- `470-extract-app-shell`
  Extract shared sidebar, header, navigation, and profile menu rendering from the main NiceGUI page module into a focused app shell module.
- `480-add-intent-comments`
  Added short intent-level comments around route orchestration, app-shell styling, controller ownership checks, and Railway deployment binding.
- `490-rename-pages-to-routes`
  Renamed the remaining route orchestration module from `ui/pages.py` to `ui/routes.py`.
- `500-clean-root-and-persistence-contract`
  Cleaned root artifacts, moved local SQLite persistence under `data/`, removed unscoped task reads, and made route registration explicit.
- `510-auth-and-contract-hardening`
  Gated development admin creation, moved registration into `AuthService`, removed inactive-user state, scoped DAO deletion, and refreshed test-case docs.
- `520-lazy-db-and-auth-boundaries`
  Made engine creation lazy, moved auth session ownership into `AuthService`, tightened task update transitions, removed ad-hoc schema alteration, and cleaned the local SQLite schema.
- `530-fix-pytest-cache-warning`
  Disabled pytest cache writes to remove sandboxed verification cache warnings.
- `540-small-hygiene-nits`
  Modernized model type hints, silenced route mypy notes with explicit return types, and removed a fake status test case.
- `550-review-hardening-followups`
  Added review-driven validation, deployment-secret, ERD, dependency-monitoring, smoke-test, and instruction-consistency hardening.
- `560-second-review-followups`
  Implemented second-review auth, filtering, task-dialog, batch-delete, notification, and validation-source cleanup.
- `570-auth-throttling-and-cleanups`
  Added login throttling, generic duplicate-email registration failures, a 10-character password floor, direct domain email validation imports, and dashboard refresh cleanup.
- `580-dashboard-refresh-and-erd-sync`
  Made dashboard refresh wiring explicit and synced the ERD artifacts to the current SQLModel ORM metadata.
- `590-collapse-task-status-states`
  Collapsed task status persistence to pending, in_progress, and done, with migration coverage for legacy created rows.

## Notes

- The roadmap is sequencing, not a status ledger.
- Update this file when prompt order or planned work changes.
