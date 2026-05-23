# 290 Remove Misleading Task Sort Control

## Scope

Remove the Tasks page `Sort by` dropdown because the List view is organized by fixed status sections: Overdue, Open, In Progress, and Done.

## Expected Files

- `src/student_task_manager/ui/pages.py`
- `docs/Status.md`
- `docs/Changelog.md`

## Tests

- Run focused UI helper tests.
- Run formatting and lint checks for the touched UI module.

## Acceptance Criteria

- The Tasks toolbar no longer shows a `Sort by` dropdown.
- Task search, status, priority, and category filters continue to work.
- List view keeps status-section grouping and due-date ordering within sections.
- Current project documentation no longer describes a sort filter as an active feature.

## Archive Condition

Archive this prompt after the implementation is verified and the app is restarted for manual review.
