# 240 Polish Task Toolbar Controls

## Scope

- Polish the Tasks toolbar search/filter/view controls.
- Keep existing filtering and view-switching behavior unchanged.

## Expected files or modules to touch

- `src/student_task_manager/ui/pages.py`
- `docs/Changelog.md`
- prompt archive files for this prompt

## Tests to add or update

- No new automated test required for styling/copy-only UI polish.

## Acceptance criteria

- Search placeholder clarifies that search is title-based.
- Toolbar controls wrap more gracefully.
- Board/List toggle is visually quieter and reads as a segmented control.
- Existing focused UI tests and lint/format checks still pass.

## Archive condition

- Archive after implementation and focused verification pass.
