# 120 Simplify Settings Page

## Objective

Keep the Settings page limited to controls that work in the current app scope.

## Scope

- Remove non-persisting Preferences, Notifications, and Appearance cards.
- Remove the notification menu footer link to notification settings.
- Keep the profile save action disabled until profile fields change.
- Move persisted user preferences to the future roadmap.
- Update current-state docs.

## Expected Files To Touch

- `src/student_task_manager/ui/pages.py`
- `docs/Roadmap.md`
- `docs/Status.md`
- `docs/Changelog.md`

## Tests To Add Or Update

- N/A. This removes non-functional UI controls and does not change task behavior.

## Acceptance Criteria

- Settings page shows only Profile and Data controls.
- Profile update is available only when the profile form has unsaved changes.
- The destructive task cleanup action is clearly labeled as deleting tasks only.
- Notification menu does not link to removed notification settings.
- Future preference persistence is documented in the roadmap.
- Repository verification gates pass.

## Archive Condition

- Repository verification gates pass.
