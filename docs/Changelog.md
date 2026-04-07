# Changelog

This file records landed repository changes.

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
