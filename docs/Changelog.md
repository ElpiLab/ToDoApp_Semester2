# Changelog

This file records landed repository changes.

## 2026-05-18

- Added a **Priority mix donut chart** to the Analytics page (ECharts) matching the Figma prototype: scoped to open ("pending") tasks, slices for High / Medium / Low with white gaps, total count + "PENDING" caption centered, and a dot-legend below. Replaces the prior horizontal-bar "By priority" card.
- Added a **Dashboard page** as the new default landing screen: stat cards (Total / Open / Completed / Overdue), "Due today" and "Coming up (next 7 days)" lists, plus In progress and High priority lists. All task items click through to the existing edit dialog. Dashboard re-renders after task save.
- Wired up the Dashboard sidebar nav item (previously a placeholder); page switching now toggles Dashboard / Tasks / Calendar panels and the workspace nav reflects the active page.
- Removed the **Modules** sidebar entry, dropping the placeholder nav item entirely.
- Updated planning docs to reflect the new state: dropped the `Module` domain entity and `020-dashboard-and-summary-queries` from the active sequence; **Analytics**, **Login**, and **Settings** are now the planned next work.
- Marked `015-consolidate-source-under-src` as the current active prompt in `Status.md` (was incorrectly listed as N/A).

## 2026-05-15

- Added a **Calendar page** with a month grid: weekday header row, day cells colored by current month, today highlight, click-to-select day, side panel listing tasks for the selected day with a per-day add-task button. Tasks render as priority-colored pills; cells overflow to a `+N more` indicator past three.
- Calendar respects task completion (strikethrough), supports prev/next month navigation, and a Today shortcut. Wired the Calendar sidebar nav item to switch panels and render on demand.

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
- Set the browser tab title to "Bizzy", autofocused the title input in the new-task dialog, repositioned `ui.notify` toasts to top-right, and added a first-run welcome empty state ("Welcome to Bizzy" + "Create your first task").
- Redesigned the task dialog to a Linear/Asana-style minimal layout: small "NEW TASK"/"EDIT TASK" caption, borderless hero title input, inline priority/due-date/status controls, collapsible description expansion, and the Delete action moved into the dialog footer for edits.
- Removed redundant `Status` enum/state plumbing left over from the earlier task-list shell so status handling collapses to a single source of truth.
- Unified status labels in the UI so both `created` and `pending` display as **"To do"** (via a shared `status_display_label` helper); board column and list badges now read consistently across views.

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
