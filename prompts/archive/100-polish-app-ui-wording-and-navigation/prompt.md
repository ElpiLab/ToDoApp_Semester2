# 100 Polish App UI Wording And Navigation

## Objective

Clean up small UI wording issues and move profile/settings controls into clearer locations.

## Scope

- Align UI wording around "To do" instead of exposing the internal "pending" label.
- Clarify Settings and notification wording.
- Move the profile avatar/menu from the header to the sidebar bottom.
- Add a Settings gear icon to the header after the notification bell.
- Remove the inactive "Mark all read" notification menu action.

## Expected Files To Touch

- `src/student_task_manager/ui/pages.py`
- `src/student_task_manager/ui/controllers.py`

## Tests To Add Or Update

- N/A. This is UI wording/layout polish with no service contract change.

## Acceptance Criteria

- Header contains a Settings icon after the notification bell.
- Sidebar contains the profile avatar/menu with Settings and Logout actions.
- Notification menu no longer shows an inactive "Mark all read" action.
- User-facing labels avoid the internal "pending" status term where practical.
- Repository verification gates pass.

## Archive Condition

- Repository verification gates pass.
