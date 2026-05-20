# Roadmap

This file tracks planned work and execution order.

## Active sequence

1. **Analytics page** (no numbered prompt yet)
   Replace the placeholder sidebar entry with a real view: charts and summary metrics over existing task data.
2. **Auth/user-scope cleanup** (no numbered prompt yet)
   Align the existing login/profile flow with task ownership so task creation and queries are scoped to the authenticated user.
3. **Login page polish** (no numbered prompt yet)
   Clean up authentication documentation and any remaining login/registration behavior after user-scoped tasks are explicit.
4. `040-settings-preferences-and-polish`
   User preferences, lower-priority settings, cleanup, and interface polish after the core flows are landed.

## Archived prompts

- `000-bootstrap-project-scaffold`
  Bootstrap scaffold, planning docs, shared agent instructions, package skeleton, and default verification setup.
- `010-task-list-view-foundation`
  Replaced the raw NiceGUI scaffold with the first structured task-list screen and improved task-flow verification.
- `015-consolidate-source-under-src`
  Moved the active application packages under `src/student_task_manager/` and made the default verification gates check the real source package.
- `020-testing-requirements-alignment`
  Added the required 12-test mix and documented the test cases in the course template format.

## Notes

- The roadmap is sequencing, not a status ledger.
- Update this file when prompt order or planned work changes.
