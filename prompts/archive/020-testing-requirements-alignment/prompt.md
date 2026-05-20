# 020 Testing Requirements Alignment

## Objective

Align the repository with the Advanced Programming testing requirement shown in the lecturer material and the Pizzeria reference project: 12 tests total, with a clear mix of unit, database, and integration tests, plus a documented test-case table.

## Scope

- keep the existing source layout under `src/student_task_manager/`
- keep this prompt focused on current task-management behavior
- add or adjust automated tests to reach this mix:
  - 6 unit tests
  - 3 database tests
  - 3 integration tests
- add `docs/TestCases.md` documenting the 12 test cases with the required fields:
  - test case ID
  - title/description
  - preconditions
  - test steps
  - test data/input
  - expected result
  - actual result
  - status
  - comments
- update `docs/Status.md`, `docs/Changelog.md`, and `docs/Roadmap.md` to reflect the landed testing state
- do not fix authentication or per-user task scoping in this prompt; record that as a known follow-up if relevant
- do not add browser automation in this prompt unless it becomes necessary for the required integration tests

## Expected files or modules to touch

- `tests/test_task_service.py`
- `tests/test_task_controllers.py`
- new: `tests/test_task_dao.py`
- new: `tests/test_task_integration.py`
- new: `docs/TestCases.md`
- `docs/Status.md`
- `docs/Changelog.md`
- `docs/Roadmap.md`

## Tests to add or update

- Unit tests should cover service/controller behavior without real database I/O.
- Database tests should use a temporary SQLite database and verify DAO persistence behavior.
- Integration tests should exercise service + DAO + SQLite together without NiceGUI browser automation.
- Preserve the package smoke test unless it makes the count unclear; document it as outside the 12-course-test mix if needed.

## Acceptance criteria

- The automated suite contains at least 12 project-behavior tests matching the required 6/3/3 mix.
- `docs/TestCases.md` maps each of the 12 required tests to an automated test function.
- The canonical verification commands pass:
  - `pytest tests/ --tb=short`
  - `ruff format --check src tests`
  - `ruff check src tests`
  - `python -m mypy src`
- `docs/Status.md` no longer implies the project lacks the required test mix.
- `docs/Changelog.md` records the testing alignment as landed.
- No authentication/user-scope behavior is silently redefined.

## Archive condition

Archive this prompt only when:

- the 12-test mix is implemented and passing
- `docs/TestCases.md` is present and complete
- the canonical verification commands pass
- planning docs reflect the current testing state honestly
