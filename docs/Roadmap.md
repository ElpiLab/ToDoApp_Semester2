# Roadmap

This file tracks planned work and execution order.

## Active sequence

1. **Login/profile polish** (no numbered prompt yet)
   Clean up authentication documentation and any remaining login/registration behavior after user-scoped tasks are explicit.
2. **UI module split** (no numbered prompt yet)
   Break down the large NiceGUI page module into smaller modules when the feature set settles.
3. **Optional export/download** (future scope)
   Add CSV/JSON task export later if it becomes useful for the final submission.

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

## Notes

- The roadmap is sequencing, not a status ledger.
- Update this file when prompt order or planned work changes.
