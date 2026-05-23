# 160 Calendar Sidebar Priority Colors

## Scope

- Fix calendar selected-day sidebar task accents so upcoming tasks use priority colors instead of always green.
- Preserve overdue-first behavior: overdue open tasks remain red regardless of priority.

## Expected files or modules to touch

- `src/student_task_manager/ui/pages.py`
- `tests/test_ui_pages.py`
- `docs/Changelog.md`
- prompt archive files for this prompt

## Tests to add or update

- Add unit coverage for calendar sidebar border class selection:
  - overdue open tasks use red
  - completed tasks use slate
  - upcoming high/medium/low tasks use priority rail colors

## Acceptance criteria

- A selected calendar day with mixed-priority upcoming tasks shows matching row accent colors in the sidebar.
- A selected calendar day with true overdue tasks still shows those rows red.
- Existing automated checks continue to pass.

## Archive condition

- Archive after implementation and relevant verification pass.
