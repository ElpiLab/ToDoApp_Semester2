# Claude Wrapper

This file is the Claude-specific wrapper for this repository.

`AGENTS.md` is the canonical shared contract. If this file conflicts with `AGENTS.md`, `AGENTS.md` wins.

## Read Order

Claude should read, in order:

1. `AGENTS.md`
2. `CLAUDE.md`
3. Relevant files under `.github/instructions/`
4. Only then the touched code and docs

## Scope

Use this file only for Claude-specific wrapper behavior. Shared workflow, planning rules, invariants, validation expectations, and repo-boundary rules live in `AGENTS.md`.

## Required Shared Instruction Files

Read the relevant files under `.github/instructions/` before making substantive changes:

- `.github/instructions/python.instructions.md` for Python code changes
- `.github/instructions/docs.instructions.md` for Markdown and planning-doc changes

Keep this wrapper aligned with `.github/copilot-instructions.md`.
