# ARCHIVE.md

Date: 2026-04-08
Author: OpenAI Codex
PR / Commit: N/A

Files changed:
- AGENTS.md
- CLAUDE.md
- .github/copilot-instructions.md
- .github/instructions/docs.instructions.md
- .github/instructions/python.instructions.md
- README.md
- .gitignore
- pyproject.toml
- docs/Roadmap.md
- docs/Status.md
- docs/Changelog.md
- prompts/templates/ARCHIVE.md
- prompts/templates/changes.json.example
- prompts/archive/000-bootstrap-project-scaffold/prompt.md
- prompts/archive/000-bootstrap-project-scaffold/ARCHIVE.md
- prompts/archive/000-bootstrap-project-scaffold/changes.json
- src/student_task_manager/__init__.py
- src/student_task_manager/app.py
- tests/conftest.py
- tests/test_smoke.py

Tests added/updated:
- tests/test_smoke.py
- tests/conftest.py

Commands run (copyable):
```bash
python -m pytest tests/ --tb=short
python -m ruff format --check src tests
python -m ruff check src tests
python -m mypy src
```

Known risks & mitigations:
- Risk: the current scaffold only establishes project structure and contributor workflow, not the task manager domain model or UI. Mitigation: start the next numbered prompt before implementation work resumes.
- Risk: external cache paths work in the normal local environment but sandboxed runs may still be unable to write outside the repo root. Mitigation: treat this as an execution-environment constraint, not a repo configuration defect.

Follow-ups / rollback notes:
- Next follow-up: create and activate `010-domain-model-and-persistence` before further coding.
- Rollback: revert this archive move together with the planning-doc updates if the bootstrap phase needs to be reopened.

Notes:
- Prompt `000` was archived after the bootstrap scaffold, shared agent instructions, and default verification checks were completed.
