# Student Task Manager

This file is the canonical instruction source for agents working in this repository.

The goal is predictable, minimal, and reviewable work across implementation, review, and documentation tasks.

## 0. Project Overview

This repository contains a browser-based student task manager for the Advanced Programming course.

Current repository status:

- the repository is still in early setup
- `README.md` defines the product scope and baseline architecture
- prompt templates exist under `prompts/templates/`
- planning docs live under `docs/`
- implementation work should be driven by the prompt workflow, not ad-hoc coding

Architecture constraints:

- UI in NiceGUI
- business logic in Python on the server
- SQLite persistence via SQLAlchemy ORM
- keep UI, business logic, and persistence clearly separated
- prefer a modular, object-oriented structure unless a simpler function-based design is clearly better for the touched code

## 1. Agent Operating Model

On every task, follow this order:

1. Read `AGENTS.md` first.
2. Read the active numbered prompt in `prompts/active/` if the task requires code changes.
3. Read only the minimum relevant source, test, and doc files needed for the task.
4. Identify the invariants and validation gates affected by the change.
5. Make the smallest correct change that preserves those invariants.
6. Run the relevant verification steps for the touched behavior.
7. Update prompts and docs when the task changes behavior, public-facing interfaces, service contracts, or the prompt workflow itself, for example a service method signature, model field, route, or UI-visible label.

Do not scan the whole repository unless the task genuinely requires it.

## 2. Instruction Precedence

When instructions conflict, apply them in this order:

1. `AGENTS.md`
2. Tool-specific wrappers such as `CLAUDE.md` and `.github/copilot-instructions.md`
3. Task-relevant repository docs
4. Task-relevant files under `.github/instructions/`, if they exist

Repository docs are listed ahead of `.github/instructions/` on purpose: this repo should keep its durable project contract in versioned project docs first, and use `.github/instructions/` only for narrower tool or domain guidance.

Keep wrapper files aligned across agents. `CLAUDE.md` and `.github/copilot-instructions.md` should point to the same shared repo contract and the same `.github/instructions/` files rather than defining separate behavior.

If two instructions still appear to conflict, prefer the more specific instruction unless it violates a higher-priority rule from this file.

## 3. Prompt Workflow

Implementation work must be driven by numbered prompts.

- Do not start coding unless there is an active, numbered prompt in `prompts/active/`.
- Review, analysis, and documentation-only tasks may proceed without an active prompt unless the user explicitly wants the prompt workflow used.
- Always work the lowest-numbered active prompt first unless the user explicitly says otherwise.
- If `prompts/active/` does not exist or has no active numbered prompt, create the next prompt before starting implementation rather than bypassing the workflow.
- Numbered prompts are execution contracts, not scratch notes.
- Keep the active prompt queue short and ordered.

Each new numbered prompt should include:

- scope
- expected files or modules to touch
- tests to add or update
- acceptance criteria
- archive condition

Prompt numbering rules:

- use a stable numeric prefix such as `000`, `010`, `020`
- numbering must reflect intended execution order
- do not renumber existing prompts purely for cosmetic cleanup unless the user explicitly requests it

## 4. Prompt Archive Rules

Do not blur planning artifact roles:

- active prompts under `prompts/active/` define still-open implementation work
- archived prompt folders under `prompts/archive/` record completed work
- `AGENTS.md` defines the repo-wide contributor contract
- `docs/Roadmap.md` tracks planned sequencing
- `docs/Status.md` tracks the current state honestly
- `docs/Changelog.md` records landed changes only

When a prompt is ready to archive:

- move the original prompt to `prompts/archive/<id>-<slug>/prompt.md`
- do not rewrite the original prompt in place to look cleaner after the fact
- add `prompts/archive/<id>-<slug>/ARCHIVE.md`
- optionally add `prompts/archive/<id>-<slug>/changes.json`

Archive only when the implementation is actually landed and verified. Do not archive a prompt merely because a scaffold, partial draft, or incomplete code path exists.

`ARCHIVE.md` should summarize:

- date completed
- author
- PR or commit SHA, if available
- files changed
- tests added or updated
- commands run
- known risks and mitigations
- follow-ups or rollback notes, if relevant

For fields with no value yet, write `N/A` rather than leaving them ambiguous or omitting them.

See `prompts/templates/` for archive templates.

If `AGENTS.md` and another planning document or prompt state different workflow rules, reconcile them explicitly in the same change rather than leaving both sources inconsistent.

## 5. Development Principles

- Prefer the smallest, well-scoped change that fixes the issue.
- Follow test-driven development where practical: add the smallest failing test first, then implement the minimum change to pass it.
- Keep UI thin: business logic belongs in services, not UI code.
- Keep persistence concerns out of UI code.
- Fail fast on programmer errors.
- Never swallow exceptions silently.
- Prefer explicit service methods over hidden side effects.
- Avoid speculative abstractions.
- Keep modules focused on one responsibility where practical.
- Keep Python source under `src/`.
- Use typed functions and dataclasses where they improve clarity.
- Every bug fix should include a regression test when feasible.

## 6. Project Invariants

These invariants outrank local implementation convenience:

1. Business rules belong in services or domain logic, not in NiceGUI page code.
2. `models.py` is the ORM source of truth for entities and constraints.
3. Engine and session creation must be centralized, for example in `session.py`.
4. Bootstrap schema from ORM metadata with `Base.metadata.create_all(engine)` unless the repository later adopts an explicit migration tool. If a migration tool is introduced, update this file through the prompt workflow before normalizing the new rule elsewhere.
5. Failed SQL writes must not be silently ignored. Surface the error with enough context to retry or diagnose it.
6. Validation errors should be explicit and actionable.
7. Temporary or generated artifacts must not accumulate in the repo root.

## 7. Verification

Run these commands before marking implementation work done:

```bash
python -m pip install -e ".[dev]"
pytest tests/ --tb=short
ruff format --check src tests
ruff check src tests
python -m mypy src
```

Verification rules:

- if a command is not yet available because the repo is still being scaffolded, say so explicitly
- prefer running checks relevant to touched files first, then the broader suite when practical
- do not proceed past a failing gate without fixing it and re-running the relevant checks
- if a check is unavailable because the repo is still being scaffolded, document the gap explicitly and leave the task marked incomplete
- do not claim a task is fully verified if commands were skipped

If the repository later adds a canonical `make verify` or equivalent wrapper, update this file to make that the default entry point.

## 8. Repo Hygiene

- Do not commit datasets, DB files, logs, caches, or other generated artifacts to the repo root.
- Keep scratch files in an ignored location such as `build/`, `tmp/`, or another documented non-root path.
- Tool caches (pytest, ruff, mypy) are stored under `C:/Users/lence/AppData/Local/ToDoApp_Semester2/`, and virtual environments should stay outside the repo. Do not move these inside the project root.
- Ensure generated-artifact paths are covered by `.gitignore` when they are expected to recur.
- Prefer editing existing files over adding new files when sensible.
- Avoid unnecessary dependencies; justify any new dependency in the PR description or archive notes.
- Never use bare `except:`.
- Encode units in variable names when units matter, for example `timeout_s` or `latency_ms`.

## 9. Key Reference Paths

Read these first when they are relevant:

- `README.md`
- the active numbered prompt under `prompts/active/`
- `docs/Roadmap.md`
- `docs/Status.md`
- `docs/Changelog.md`
- `prompts/templates/ARCHIVE.md`
- `prompts/templates/changes.json.example`

Update this section when more project docs become canonical.

## 10. Task Completion Checklist

A task is not complete until all relevant items below are addressed or explicitly marked not applicable:

- code change implemented and minimal
- tests added or updated
- relevant docs or prompts updated
- project invariants preserved
- validation performed and reported per Section 7
- prompt archived when implementation work tied to that prompt is complete
- known risks or follow-ups recorded when applicable

## 11. When In Doubt

If you are unsure about an invariant, architecture choice, or workflow rule:

- prefer the smaller change
- document the assumption
- open or refine a prompt instead of inventing hidden scope
- keep the active prompt queue short and actionable
