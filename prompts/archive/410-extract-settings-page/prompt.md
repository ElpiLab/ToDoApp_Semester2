# 410 Extract Settings Page

## Scope

Move the Settings page renderer out of `src/student_task_manager/ui/pages.py` into a focused settings module.

## Expected Files

- `src/student_task_manager/ui/pages.py`
- `src/student_task_manager/ui/settings_page.py`
- `docs/Changelog.md`
- `docs/Roadmap.md`
- `docs/Status.md`
- `prompts/archive/410-extract-settings-page/`

## Tests

- Run the focused UI tests after extraction.
- Run the full verification gates before completion.

## Acceptance Criteria

- Settings page behavior remains unchanged:
  - profile update still validates name and email
  - password change still validates all fields
  - delete-all flow still confirms before deleting tasks
- `pages.py` delegates settings rendering to the extracted module.
- No task, calendar, or analytics behavior is changed.
- Documentation and prompt archive are updated.

## Archive Condition

Archive this prompt after the extraction is implemented, verified, and ready for commit.
