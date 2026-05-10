# 010 Task List View Foundation

## Objective

Replace the current free-form NiceGUI scaffold with the first intentional application slice: a Figma-aligned task list experience built on the existing task domain and service flow.

## Scope

- introduce a structured application shell for the first usable screen
- make `Task List View` the primary implementation target instead of the current always-visible form scaffold
- move task creation into a modal, drawer, or similarly contained interaction
- present tasks in a structured list or table with clear columns and actions
- keep filtering and search, but place them inside a coherent toolbar above the task list
- preserve the service-layer boundary for business rules and avoid pushing domain logic into NiceGUI page code
- reduce direct UI-to-DAO coupling where it is touched by this work
- keep the implementation limited to the first vertical slice; do not add dashboard, calendar, analytics, or board-specific interactions in this prompt

## Expected files or modules to touch

- `application.py`
- `ui/pages.py`
- `ui/controllers.py`
- `services/task_service.py`
- `domain/models.py`
- `data_access/dao.py`
- `data_access/db.py`
- `tests/`
- `docs/Status.md`
- `docs/Changelog.md`

## Tests to add or update

- add or update service and UI-adjacent regression tests covering task creation and listing behavior
- add at least one test covering the touched validation or update flow if the current implementation path changes

## Acceptance criteria

- the app opens to a deliberate `Task List View` rather than an unstructured scaffold
- task creation is no longer permanently exposed as raw inputs at the top of the page
- the main screen has clear layout hierarchy, with navigation or shell structure and a dedicated task-content area
- users can create, list, edit, complete, delete, filter, and search tasks using the updated screen
- persistence continues to work with the existing SQLite-backed flow
- touched task mutations flow through an explicit service boundary rather than introducing more UI-to-DAO shortcuts
- tests cover the changed behavior at the appropriate level for the touched code
- `Status.md` and `Changelog.md` reflect the landed state honestly when this prompt is completed

## Archive condition

Archive this prompt only when the first task-list slice is landed, verified, and clearly replaces the current scaffold as the default user experience. Do not archive it while the page is still primarily a raw form-on-blank-canvas prototype or while task mutations still rely on newly introduced architectural shortcuts.
