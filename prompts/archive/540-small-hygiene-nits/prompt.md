# 540 Small Hygiene Nits

## Scope

Clean up small non-behavioral issues left after the persistence and pytest-cache work.

## Expected Files or Modules to Touch

- `src/student_task_manager/domain/models.py`
- `src/student_task_manager/ui/routes.py`
- `tests/test_ui_pages.py`
- planning and archive docs

## Tests to Add or Update

- Update the UI helper test that used a non-existent status value.

## Acceptance Criteria

- Domain models use PEP 604 collection/optional typing.
- `mypy` no longer emits annotation-unchecked notes for `routes.py`.
- UI helper tests no longer rely on a fake `overdue` status value.
- Verification gates remain green.

## Archive Condition

Archive after verification passes.
