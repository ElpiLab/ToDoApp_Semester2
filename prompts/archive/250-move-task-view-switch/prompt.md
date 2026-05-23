# 250 Move Task View Switch

## Scope

- Move the Tasks Board/List view switch out of the filter row.
- Label it as a view switch beside the Tasks heading.
- Keep existing Board/List behavior unchanged.

## Expected files or modules to touch

- `src/student_task_manager/ui/pages.py`
- `docs/Changelog.md`
- prompt archive files for this prompt

## Tests to add or update

- No new automated test required for layout-only UI polish.

## Acceptance criteria

- Board/List no longer wraps under the filters in List view.
- The switch has a nearby `View` label so users understand it changes the task view.
- Existing focused UI tests and lint/format checks still pass.

## Archive condition

- Archive after implementation and focused verification pass.
