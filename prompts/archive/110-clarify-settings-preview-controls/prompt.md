# 110 Clarify Settings Preview Controls

## Objective

Make Settings controls honest when they are visible but not saved yet.

## Scope

- Update Settings helper text so temporary controls are described as not saved yet, rather than session-persistent.
- Keep existing Settings behavior unchanged.

## Expected Files To Touch

- `src/student_task_manager/ui/pages.py`

## Tests To Add Or Update

- N/A. UI copy only.

## Acceptance Criteria

- Preferences, Notifications, and Appearance cards clearly state that their controls are not saved yet.
- Email reminder copy does not imply the current logged-in user still needs to log in.
- Repository verification gates pass.

## Archive Condition

- Repository verification gates pass.
