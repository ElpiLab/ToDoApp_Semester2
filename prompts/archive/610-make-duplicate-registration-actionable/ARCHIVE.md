# Archive Summary

Date completed: 2026-05-24
Author: Codex
PR or commit SHA: 25bd81e

## Files Changed

- `docs/Changelog.md`
- `docs/Roadmap.md`
- `src/student_task_manager/ui/registration.py`
- `tests/test_browser_smoke.py`
- `prompts/archive/610-make-duplicate-registration-actionable/ARCHIVE.md`
- `prompts/archive/610-make-duplicate-registration-actionable/prompt.md`

## Tests Added or Updated

- `tests/test_browser_smoke.py::test_duplicate_registration_stays_on_registration_page`

## Commands Run

```bash
pytest tests/test_browser_smoke.py tests/test_auth_service.py --tb=short
python -m pip install -e ".[dev]"
pytest tests/ --tb=short
ruff format src tests
ruff format --check src tests
ruff check src tests
python -m mypy src
git diff --check
```

## Known Risks and Mitigations

- Risk: This makes duplicate registration behavior visibly different from successful new registration. Mitigation: the message still does not expose account data or passwords, and the app has no email-confirmation or password-reset flow, so the previous success-like behavior was actively misleading.

## Follow-ups or Rollback Notes

- A password reset flow would be the proper long-term answer for users who already registered and forgot their password.
