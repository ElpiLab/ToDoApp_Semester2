# 420 Extract Calendar Page

## Scope

Move the Calendar page renderer out of `src/student_task_manager/ui/pages.py` into a focused calendar module.

## Expected Files

- `src/student_task_manager/ui/pages.py`
- `src/student_task_manager/ui/calendar_page.py`
- `docs/Changelog.md`
- `docs/Roadmap.md`
- `docs/Status.md`
- `prompts/archive/420-extract-calendar-page/`

## Tests

- Run the focused UI tests after extraction.
- Run the full verification gates before completion.

## Acceptance Criteria

- Calendar behavior remains unchanged:
  - month navigation still works
  - Today still returns to the current month and selected date
  - selecting a day still updates the sidebar
  - empty-day and task-day sidebar actions keep the current wording
  - per-day add-task buttons still open the task dialog with the selected due date
- `pages.py` delegates calendar rendering to the extracted module.
- No task, dashboard, analytics, or settings behavior is changed.
- Documentation and prompt archive are updated.

## Archive Condition

Archive this prompt after the extraction is implemented, verified, and ready for commit.
