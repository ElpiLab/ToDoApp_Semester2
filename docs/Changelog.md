# Changelog

This file records landed repository changes.

## 2026-05-10

- Added a **Board view** (To do / In progress / Done) as the default Tasks layout, with a Board/List toggle for switching.
- Implemented **drag-and-drop** between board columns; dropping a card updates the task status. Target column highlights teal during drag.
- Added per-column empty states ("Nothing in progress", "No completed tasks yet") and a `+ Add task` placeholder at the bottom of To do.
- Replaced the All/Open/Completed filter toggle with **Status / Priority / Sort by dropdowns**; wired the global header search to filter tasks live.
- Restructured the Tasks page: removed summary cards and the inner Tasks card wrapper. The page is now heading + toolbar + view container.
- Polished the new-task dialog: hero title input, LOW/MED/HIGH segmented priority, collapsible description, "Add another" checkbox, real date picker.
- Polished the sidebar and header chrome: WORKSPACE/SYSTEM sections, real per-item icons, lightning-bolt brand mark, user chip, full-width separator. Drawer extends above the header.
- Cleaner Asana-style cards on the board: click anywhere to edit, no visible action buttons. Destructive actions live in the edit dialog with a **confirmation dialog before delete**.
- Polished the list view to match: row hover, click-to-edit, relative due dates ("Due 14 May · in 4 days"), red-bold for late, strikethrough for done, smaller icon-only actions with hover tooltips.
- Relaxed `TaskService._normalize_description` so descriptions are now optional (was min 5 chars).
- Added `change_task_status(task_id, target_status)` controller used by drag-drop.
- Made the date parser tolerant of `2026.05.14` and `2026/05/14` formats in addition to ISO `2026-05-14`.

## 2026-05-09

- Added active prompt `010-task-list-view-foundation` and aligned planning docs with the actual implementation state.
- Reworked the NiceGUI home page into a structured task-list shell with sidebar navigation, summary cards, toolbar controls, and dialog-based task creation/editing.
- Removed the UI-to-DAO update shortcut by routing task updates through `TaskService`.
- Added regression tests covering task-service state transitions and controller update/create flows.
- Declared the missing runtime dependencies in `pyproject.toml` for `nicegui` and `sqlmodel`.

## 2026-04-08

- Archived `000-bootstrap-project-scaffold` under `prompts/archive/000-bootstrap-project-scaffold/` and cleared the active prompt queue.

## 2026-04-07

- Added initial planning surfaces: `docs/Roadmap.md`, `docs/Status.md`, and `docs/Changelog.md`.
- Initialized the prompt workflow with `prompts/active/000-bootstrap-project-scaffold.md`.
- Expanded `AGENTS.md` to define planning artifact roles and reference the new planning docs.
- Added shared agent wrappers and instruction files for Claude and Copilot / Codex.
- Added the initial Python project scaffold: `pyproject.toml`, `.gitignore`, `src/student_task_manager/`, and `tests/`.
- Added a smoke test and test bootstrap so the local package resolves from this repository during test runs.
- Moved tool caches to `C:/Users/lence/AppData/Local/ToDoApp_Semester2/` and verified the default bootstrap checks in the local environment.
