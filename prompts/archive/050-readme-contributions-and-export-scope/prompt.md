# 050 README Contributions and Export Scope

## Objective

Keep the README aligned with the course/reference-project style by adding a Team Contributions section and a concise future roadmap, and remove export/download actions from the current UI so analytics remains view-only for this scope.

## Scope

- add a `Team Contributions` section to `README.md` with contribution cells left blank
- add a concise future roadmap section to `README.md`
- remove CSV/JSON export/download controls and helper functions from the NiceGUI settings UI
- keep analytics as a view-only summary
- update planning docs and changelog
- do not redesign analytics or settings in this prompt

## Expected files to touch

- `README.md`
- `src/student_task_manager/ui/pages.py`
- `docs/Status.md`
- `docs/Changelog.md`
- `docs/Roadmap.md`

## Tests to add or update

- No new automated tests expected unless removing export changes tested behavior.

## Acceptance criteria

- README includes blank Team Contributions rows.
- README includes future roadmap items that are clearly not yet implemented.
- UI no longer offers task export/download actions.
- Analytics remains view-only.
- Verification passes:
  - `pytest tests/ --tb=short`
  - `ruff format --check src tests`
  - `ruff check src tests`
  - `python -m mypy src`

## Archive condition

Archive this prompt only after the README and UI scope changes are complete, documented, and verified.
