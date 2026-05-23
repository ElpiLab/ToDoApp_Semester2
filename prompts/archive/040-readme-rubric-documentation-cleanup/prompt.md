# 040 README Rubric Documentation Cleanup

## Objective

Rewrite the README and related planning docs so the project is easy to understand and grade against the Advanced Programming rubric and the lecturer's Pizzeria reference project.

## Scope

- replace outdated README content with current, accurate project documentation
- clearly separate implemented behavior from planned/future work
- document the `src/student_task_manager/` package layout and map it to the reference architecture layers
- document current database entities from `src/student_task_manager/domain/models.py`
- document setup, run, and verification commands
- document the 12-test rubric mix and link to `docs/TestCases.md`
- remove duplicate or stale user stories and references to entities that are not implemented
- update `docs/Status.md`, `docs/Changelog.md`, and `docs/Roadmap.md` if needed
- do not change application behavior in this prompt

## Expected files to touch

- `README.md`
- `docs/Status.md`
- `docs/Changelog.md`
- `docs/Roadmap.md`

## Tests to add or update

- No automated test changes expected.
- Run the canonical verification commands to confirm documentation-only edits did not disturb the project.

## Acceptance criteria

- README accurately describes the current Bizzy student task manager.
- README explains the source layout and why `src/student_task_manager/` corresponds to the app package.
- README documents the current SQLModel entities: `Student`, `Task`, `Priority`, and `Status`.
- README includes setup/run/test commands.
- README links to `docs/TestCases.md`.
- Planning docs reflect that README/rubric documentation cleanup is complete.
- Verification commands pass:
  - `pytest tests/ --tb=short`
  - `ruff format --check src tests`
  - `ruff check src tests`
  - `python -m mypy src`

## Archive condition

Archive this prompt only when the README is updated, relevant docs are current, and verification passes.
