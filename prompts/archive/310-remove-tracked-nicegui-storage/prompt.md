# 310 Remove Tracked NiceGUI Runtime Storage

## Scope

Remove generated NiceGUI per-user runtime storage files from version control.

## Expected Files

- `.nicegui/storage-user-*.json`
- `docs/Changelog.md`
- `docs/Status.md`

## Tests

- Run the full automated test suite.
- Run format, lint, and type checks.

## Acceptance Criteria

- No `.nicegui` runtime storage files are tracked by Git.
- `.gitignore` continues to ignore `.nicegui/`.
- Verification gates pass.

## Archive Condition

Archive this prompt after cleanup and verification are complete.
