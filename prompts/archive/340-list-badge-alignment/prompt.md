# 340 List Badge Alignment

## Scope

Align the priority and status badges in Tasks List view so LOW, MED, HIGH, and the status pills line up consistently across rows.

## Expected Files

- `src/student_task_manager/ui/pages.py`
- `docs/Changelog.md`
- `docs/Status.md`

## Tests

- Run the UI test module and full verification gates.
- No new automated regression test is expected because this is a layout-only class change.

## Acceptance Criteria

- Priority badges in List view share a fixed visual column.
- Status pills in List view share a fixed visual column.
- Task title/description content still truncates instead of pushing badges out of alignment.
- Existing task behavior is unchanged.

## Archive Condition

Archive this prompt after implementation, verification, documentation updates, commit, and push are complete.
