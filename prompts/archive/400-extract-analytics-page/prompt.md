# 400 Extract Analytics Page

## Scope

Move the analytics page rendering code out of `src/student_task_manager/ui/pages.py` into a focused UI module.

## Expected Files

- `src/student_task_manager/ui/pages.py`
- `src/student_task_manager/ui/analytics_page.py`
- `docs/Changelog.md`
- `docs/Roadmap.md`
- `docs/Status.md`
- `prompts/archive/400-extract-analytics-page/`

## Tests

- Run targeted UI tests after extraction.
- Run the full project verification gates before archiving.

## Acceptance Criteria

- `pages.py` still owns route setup, state, and panel switching.
- The analytics page UI is rendered through a focused function in `analytics_page.py`.
- The analytics screen remains visually and functionally unchanged.
- No business logic or persistence code is moved into the UI module.
- Existing tests and quality gates pass.

## Archive Condition

Archive this prompt after implementation, documentation updates, and verification are complete.
