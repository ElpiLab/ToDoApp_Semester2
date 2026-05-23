# 130 Polish Notification Bell

## Objective

Make the notification bell and dropdown clearer without adding database-backed notification persistence.

## Scope

- Keep the bell badge as an unread dot.
- Add session-level read actions for generated notifications.
- Make the notification menu size content naturally and scroll when needed.
- Improve the empty notification message.

## Expected Files To Touch

- `src/student_task_manager/ui/pages.py`

## Tests To Add Or Update

- N/A. UI polish only.

## Acceptance Criteria

- The bell badge appears only when at least one notification is unread.
- The notification menu lets users mark individual notifications or all current notifications as read for the current session.
- The notification menu no longer reserves excessive empty height.
- Empty notification state explains what "caught up" means.
- Repository verification gates pass.

## Archive Condition

- Repository verification gates pass.
