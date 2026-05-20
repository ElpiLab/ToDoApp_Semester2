# 040 README Rubric Documentation Cleanup Archive

Date: 2026-05-20
Author: Codex
PR / Commit: N/A

Files changed:
- README.md
- docs/Status.md
- docs/Roadmap.md
- docs/Changelog.md

Tests added or updated:
- N/A

Commands run:
```bash
pytest tests/ --tb=short
ruff format --check src tests
ruff check src tests
python -m mypy src
```

Known risks and mitigations:
- Risk: The README documents current behavior but does not replace the older ERD image/assets. Mitigation: it names `src/student_task_manager/domain/models.py` as the ORM source of truth.
- Risk: NiceGUI browser flows remain manually tested. Mitigation: README and status docs describe the automated test boundary honestly.
- Risk: `pytest` still reports a cache write warning for `C:/Users/lence/AppData/Local/ToDoApp_Semester2/pytest_cache`. Mitigation: the suite itself passed.

Follow-ups / rollback notes:
- Future documentation updates should keep implemented behavior separate from planned work.
- If the course requires the flat package layout used by the Pizzeria reference project, document the `src/` layout explanation before changing code structure.
