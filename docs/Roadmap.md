# Roadmap

This file tracks planned work and execution order.

## Active sequence

1. **Login/profile polish** (no numbered prompt yet)
   Clean up authentication documentation and any remaining login/registration behavior after user-scoped tasks are explicit.
2. **UI module split** (no numbered prompt yet)
   Break down the large NiceGUI page module into smaller modules when the feature set settles.
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

## Notes

- The roadmap is sequencing, not a status ledger.
- Update this file when prompt order or planned work changes.
