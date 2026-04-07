---
applyTo: "**/*.py"
---
# Python Instructions

Use this file for Python source and test changes.

## Core Rules

- Follow the repo-wide contract in `AGENTS.md` first.
- Use the Python version enforced in `pyproject.toml`.
- Add type hints for public APIs and non-trivial internal APIs when they improve clarity.
- Keep business logic out of UI code.
- Isolate I/O at system boundaries when practical.
- Avoid hidden global mutable state.
- Use `dataclasses` for small record-like types when they fit better than loosely shaped dictionaries.
- Prefer `pathlib` and context managers for filesystem and resource lifetimes.
- Validate untrusted input at boundaries.
- Catch specific exceptions with actionable context.
- Never use bare `except:`.

## Style

- Formatting is mandatory with ruff.
- Line length is 100.
- Prefer `snake_case` for files, variables, and functions.
- Avoid mutable default arguments.
- Prefer small cohesive functions over large multi-purpose functions.
- Comments should explain why, not restate what the code does.

## Architecture

- Keep Python source under `src/`.
- Keep UI thin and place business rules in services or domain logic.
- Treat `models.py` as the ORM source of truth for entities and constraints.
- Centralize engine and session creation.
- Use explicit exceptions for runtime validation; use `assert` only for programmer invariants.

## Validation

- Run `python -m pip install -e ".[dev]"` when setting up or refreshing the local development environment; it is environment setup, not a per-change code-quality gate.
- Run `pytest tests/ --tb=short` for the default gate.
- Use `ruff format --check src tests` and `ruff check src tests` for hygiene.
- Run `python -m mypy src` when type checks are available for the touched code.
- Every bug fix should include a regression test when feasible.

## Testing

- Add tests for behavior, not implementation details.
- Keep the default suite fast.
- Prefer deterministic tests where practical.
- Use `tests/` for the default quick suite unless the repo later introduces explicit non-default test buckets.
