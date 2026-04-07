---
applyTo: "**/*.md"
---
# Documentation Instructions

Use this file for Markdown docs, prompts, and planning-surface updates.

## General Rules

- Follow `AGENTS.md` first.
- Prefer short sections with headings and flat lists over long dense paragraphs.
- Keep commands copy-paste runnable.
- Keep examples minimal but complete.
- Update docs in the same change as behavior or workflow changes.

## Planning Artifact Roles

- `AGENTS.md` defines the repo-wide contributor contract.
- `prompts/active/` contains still-open implementation prompts.
- `prompts/archive/` records completed prompts and archive summaries.
- `docs/Roadmap.md` tracks planned sequencing.
- `docs/Status.md` tracks the current state honestly.
- `docs/Changelog.md` records landed changes only.

Do not blur those roles.

## Prompt Docs

- Numbered prompts are execution contracts, not topic notes.
- Good prompts state objective, scope, touched areas, tests, acceptance criteria, and archive condition.
- Archive prompts only when implementation is landed and verified.

## Update Patterns

- Update `Roadmap` when planned order or future work changes.
- Update `Status` when the current repo state changes.
- Update `Changelog` only for landed workflow, code, or contract changes.
- If `AGENTS.md` and another planning document disagree, reconcile them in the same change.
