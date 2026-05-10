# 015 Consolidate Source Under src/

## Objective

Bring the active implementation in line with the repo contract by consolidating the four top-level Python packages (`domain/`, `services/`, `data_access/`, `ui/`) into a single installable package under `src/student_task_manager/`. Verification gates from `AGENTS.md` (`pytest`, `ruff`, `mypy src`) should operate on the real application code afterward, not on a parallel empty package.

## Scope

- move `domain/`, `services/`, `data_access/`, and `ui/` from the repository root into `src/student_task_manager/` as subpackages, preserving their internal module structure
- update every import inside the moved code to reference the new `student_task_manager.*` package paths
- update `application.py` so it still works as the entry point but imports from `student_task_manager.*`
- update tests under `tests/` to import from the new package paths and drop the `sys.path` shim in `tests/conftest.py` once the package resolves naturally through the editable install
- remove the now-empty top-level `__init__.py` at the repository root and any other stale top-level package markers left behind by the move
- keep `application.py` at the repository root for now; do not redesign the entry-point story in this prompt
- do not change UI behavior, validation rules, ORM models, database schema, or any business logic
- do not introduce new entities (no `Module`, no `Student`) — those belong to a later prompt
- do not redesign verification commands; only adjust the targets they point at where the move requires it
- do not migrate to a different package name or rename `student_task_manager`

## Expected files or modules to touch

- `application.py`
- `pyproject.toml` (only if the move actually requires a config change — current `package-dir`/`packages.find` already point at `src/`, so confirm no edit is needed and note it explicitly if so)
- `src/student_task_manager/__init__.py`
- new: `src/student_task_manager/domain/...` (moved from `domain/`)
- new: `src/student_task_manager/services/...` (moved from `services/`)
- new: `src/student_task_manager/data_access/...` (moved from `data_access/`)
- new: `src/student_task_manager/ui/...` (moved from `ui/`)
- delete: top-level `domain/`, `services/`, `data_access/`, `ui/` directories after the move
- delete: top-level `__init__.py` if it remains empty after the move
- `tests/conftest.py`
- `tests/test_smoke.py`
- `tests/test_task_service.py`
- `tests/test_task_controllers.py`
- `docs/Status.md`
- `docs/Changelog.md`
- `docs/Roadmap.md` (only to reflect that the structural cleanup landed; do not reorder the dashboard / board / settings sequence)

## Tests to add or update

- update existing service and controller tests so they import from `student_task_manager.*`; the test bodies should not change in behavior
- keep `tests/test_smoke.py` exercising the package version, but make sure it is the only test relying on the bare `student_task_manager` import surface
- add at least one regression-level assertion (existing or new) that fails if the package layout silently regresses — for example, a test that imports `student_task_manager.services.task_service.TaskService` directly and instantiates it with a fake DAO
- do not add new domain or UI tests in this prompt; coverage growth is out of scope here

## Acceptance criteria

- a fresh checkout can run the verification commands from `AGENTS.md` Section 7 successfully against the new layout, with mypy and ruff both targeting `src` and `tests`
- `python application.py` (or the equivalent module-level entry) still launches the existing Task List View and all current task CRUD interactions continue to work end-to-end against the SQLite database
- no Python module under the repository root remains importable as `domain`, `services`, `data_access`, or `ui`; the only canonical import root for application code is `student_task_manager`
- `tests/conftest.py` no longer manipulates `sys.path`; tests resolve the package through the editable install instead
- `docs/Status.md` no longer claims the source layout drifts from the repo contract
- `docs/Changelog.md` records the move as a single entry, not a series of speculative cleanup notes
- the project invariants in `AGENTS.md` Section 6 are preserved; in particular, business rules still live in `student_task_manager.services`, ORM definitions still live in `student_task_manager.domain.models`, and engine creation is still centralized in `student_task_manager.data_access.db`
- no new dependencies are introduced

## Archive condition

Archive this prompt only when:

- the four packages are physically moved under `src/student_task_manager/`
- every import statement in `application.py`, the moved code, and the test suite uses the new package path
- all four verification commands from `AGENTS.md` Section 7 run green from a clean working tree
- `docs/Status.md`, `docs/Changelog.md`, and (where relevant) `docs/Roadmap.md` reflect the landed state honestly

Do not archive this prompt while a parallel top-level copy of `domain/`, `services/`, `data_access/`, or `ui/` still exists, while tests still depend on `sys.path` manipulation, or while `application.py` still imports from the old top-level paths.
