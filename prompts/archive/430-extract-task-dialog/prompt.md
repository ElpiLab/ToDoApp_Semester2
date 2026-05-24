# 430 Extract Task Dialog

## Scope

Move the task create/edit dialog renderer out of `src/student_task_manager/ui/pages.py` into a focused dialog module.

## Expected Files

- `src/student_task_manager/ui/pages.py`
- `src/student_task_manager/ui/task_dialog.py`
- `docs/Changelog.md`
- `docs/Roadmap.md`
- `docs/Status.md`
- `prompts/archive/430-extract-task-dialog/`

## Tests

- Run the focused UI tests after extraction.
- Run the full verification gates before completion.

## Acceptance Criteria

- Task dialog behavior remains unchanged:
  - creating tasks still works
  - editing tasks still works
  - deleting tasks still confirms before removal
  - Add another still keeps the dialog open and clears fields
  - default due date from Calendar still pre-fills the dialog
  - task status selection still appears only when editing
- `pages.py` delegates task dialog rendering to the extracted module.
- Board/List, Dashboard, Calendar, Analytics, and Settings behavior is unchanged.
- Documentation and prompt archive are updated.

## Archive Condition

Archive this prompt after the extraction is implemented, verified, and ready for commit.
