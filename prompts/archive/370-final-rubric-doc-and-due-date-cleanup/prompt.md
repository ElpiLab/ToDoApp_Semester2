# 370 Final Rubric Doc And Due Date Cleanup

## Scope

Make the final pre-upload cleanup requested during rubric review:

- keep new task due dates optional by default
- sync roadmap archived prompt records with the actual prompt archive
- clarify README team contributions, including the custom AI-agent prompt/workflow support

## Expected Files

- `src/student_task_manager/ui/pages.py`
- `README.md`
- `docs/Roadmap.md`
- `docs/Changelog.md`

## Tests

- Run the focused UI test module if practical.
- Run the full verification gates before archiving if time allows.

## Acceptance Criteria

- Creating a new task without a selected date no longer silently defaults to today.
- `docs/Roadmap.md` records archived prompts through `360-fix-task-category-other-option`.
- README team contributions are filled and do not overstate AI-agent use.
- Changelog records the landed cleanup.

## Archive Condition

Archive this prompt after the code/docs changes are implemented and relevant verification has passed or any skipped verification is documented.
