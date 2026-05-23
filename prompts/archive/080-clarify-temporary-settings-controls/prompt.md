# 080 Clarify Temporary Settings Controls

## Objective

Make the Settings page honest about controls that are visible but not persisted yet.

## Scope

- Add session-only caveats to the Notifications and Appearance settings cards.
- Do not implement persistence in this prompt.

## Expected Files To Touch

- `src/student_task_manager/ui/pages.py`

## Tests To Add Or Update

- N/A. This is a UI text clarification with no behavior change.

## Acceptance Criteria

- Preferences, Notifications, and Appearance cards all make their temporary/session-only behavior clear.
- Existing Settings behavior remains unchanged.

## Archive Condition

- Repository verification gates pass.
