# 590 Collapse Task Status States

## Scope

Collapse the task status model to the three states the product actually exposes: `pending`, `in_progress`, and `done`.

## Expected Files or Modules to Touch

- `src/student_task_manager/domain/models.py`
- `src/student_task_manager/services/task_service.py`
- `src/student_task_manager/ui/view_helpers.py`
- `src/student_task_manager/ui/tasks_page.py`
- `src/student_task_manager/ui/task_dialog.py`
- persistence bootstrap or migration helpers for existing `created` rows
- relevant tests and docs

## Tests to Add or Update

- Update service/UI tests that expect newly created tasks to use `created`.
- Add or update a persistence/bootstrap test that existing `created` rows are migrated to `pending`.

## Acceptance Criteria

- `Status.created` is removed from the domain enum.
- Newly created tasks persist as `pending`.
- UI status labels, filters, board grouping, dialog options, notifications, and analytics no longer need `created` compatibility logic.
- Existing SQLite rows with `status = 'created'` are migrated to `pending` before normal app use.
- Verification gates pass.

## Archive Condition

Archive after implementation, docs update, and successful verification.
