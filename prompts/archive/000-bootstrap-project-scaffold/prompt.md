# 000 Bootstrap Project Scaffold

## Objective

Create the initial repository scaffold so implementation work can begin under a defined contributor contract and prompt workflow.

## Scope

- establish the repo-wide contributor contract in `AGENTS.md`
- create the prompt workflow directories and archive templates
- create the starter planning docs: `Roadmap`, `Status`, and `Changelog`
- create shared agent-wrapper and instruction files so Claude and Copilot / Codex use the same repo contract
- create the minimal Python project structure needed to support future implementation
- create the minimal test structure and ignore rules required for local development
- configure local tooling so caches and virtual environments stay outside the repo where practical
- keep the initial scaffold small and aligned with `README.md` and `AGENTS.md`

## Expected files or modules to touch

- `AGENTS.md`
- `docs/Roadmap.md`
- `docs/Status.md`
- `docs/Changelog.md`
- `CLAUDE.md`
- `.github/copilot-instructions.md`
- `.github/instructions/docs.instructions.md`
- `.github/instructions/python.instructions.md`
- `prompts/active/`
- `prompts/archive/`
- `prompts/templates/ARCHIVE.md`
- `prompts/templates/changes.json.example`
- `.gitignore`
- `pyproject.toml`
- `src/student_task_manager/__init__.py`
- `src/student_task_manager/app.py`
- `tests/conftest.py`
- `tests/test_smoke.py`

## Tests to add or update

- add a minimal smoke test proving the package imports cleanly

## Acceptance criteria

- `AGENTS.md` defines the contributor contract, prompt workflow, planning artifact roles, and verification expectations
- Claude and Copilot / Codex wrapper files exist and point to the same shared repo contract
- prompt workflow directories exist and are tracked in git
- planning docs exist and describe the repo honestly
- prompt `000` exists and describes the bootstrap scope concretely
- Python project metadata exists
- minimal `src/` and `tests/` layout exists
- at least one test runs successfully in the current environment
- cache configuration keeps tool-generated state outside the repo where practical

## Archive condition

Archive this prompt only when the scaffold is landed, verified as far as the repo state allows, and the planning docs reflect the new baseline honestly. Do not archive it while core bootstrap items from this prompt are still missing or only partially configured.
