# 060 Fix Windows App Startup

## Objective

Fix local app startup on Windows terminals that cannot print emoji characters, and reduce noisy SQL debug output during normal app startup.

## Scope

- Replace emoji startup `print` messages with ASCII text.
- Disable SQLAlchemy echo logging for the normal SQLite engine.
- Keep application behavior unchanged.
- Update planning docs and changelog.

## Expected files to touch

- `application.py`
- `src/student_task_manager/data_access/db.py`
- `docs/Status.md`
- `docs/Changelog.md`
- `docs/Roadmap.md`

## Tests to add or update

- No new automated tests expected unless a small startup smoke check is practical.

## Acceptance criteria

- `python application.py` no longer crashes from `UnicodeEncodeError` in a Windows `cp1252` console.
- SQLAlchemy startup logs no longer flood the terminal during normal app use.
- Existing verification passes.

## Archive condition

Archive after the startup fix is implemented, verified, and documented.
