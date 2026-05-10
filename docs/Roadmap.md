# Roadmap

This file tracks planned work and execution order.

## Active sequence

1. **`Module` domain entity** (owned by teammate; no numbered prompt yet)
   Adds `Module` to the domain with a nullable FK from `Task`. Required before the dashboard, modules page, and module-aware filters/tags can land.
2. `020-dashboard-and-summary-queries`
   Add a dashboard backed by real task and module data rather than placeholder cards.
3. `030-board-and-calendar-views`
   The board portion landed as part of the Tasks page polish on 2026-05-10. This prompt now covers the **calendar view** and any board-view follow-ups.
4. `040-settings-preferences-and-polish`
   Add lower-priority settings, preferences, cleanup, and interface polish after the core flows are landed.

## Archived prompts

- `000-bootstrap-project-scaffold`
  Bootstrap scaffold, planning docs, shared agent instructions, package skeleton, and default verification setup.
- `010-task-list-view-foundation`
  Replaced the raw NiceGUI scaffold with the first structured task-list screen and improved task-flow verification.

## Notes

- The roadmap is sequencing, not a status ledger.
- Update this file when prompt order or planned work changes.
