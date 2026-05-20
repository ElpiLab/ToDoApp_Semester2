# 140 Dashboard Progress Card

## Objective

Make the dashboard completion card useful for large task histories by showing progress percentage instead of a raw lifetime completed-task count.

## Scope

- Replace the dashboard `DONE` card with a `PROGRESS` card.
- Show due-this-week completion percentage as the main value.
- Show completed/total due-this-week task count as supporting text.
- Add a small pure helper and tests for the label calculation.

## Expected Files To Touch

- `src/student_task_manager/ui/pages.py`
- `tests/test_ui_pages.py`
- `docs/Changelog.md`
- `docs/Roadmap.md`
- `docs/Status.md`

## Tests To Add Or Update

- Add unit tests for the dashboard progress label helper.

## Acceptance Criteria

- The dashboard no longer shows a large raw lifetime completed count as the main card value.
- The progress card communicates due-this-week completion percentage and completed/total due-this-week task count.
- Repository verification gates pass.

## Archive Condition

- Repository verification gates pass and this prompt is moved to `prompts/archive/140-dashboard-progress-card/`.
