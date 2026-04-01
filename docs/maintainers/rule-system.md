# Rule System

This page explains the current packaged-rule model and how it differs from workspace-local rule additions.

## Current Model

- The packaged rule corpus under `src/agentic/resources/rules/` is shared source-of-truth guidance that ships with `agentic`.
- Workspace sync mirrors those packaged rule documents into the generated project contract under `agentic/rules/`.
- True workspace-local additions live under generated folders such as `agentic/rules/overrides/` and `agentic/rules/project/`.
- Those workspace-local additions are not resolved into an effective merged rule set by current runtime code.
- The packaged `src/agentic/resources/rules/local/` branch is obsolete under this model and should not remain as shipped pseudo-local guidance.

## Metadata Status

- `tightens_paths` and `escalation_paths` exist in the frontmatter model and may support future resolver behavior.
- Current runtime code does not use those fields to compute merged rule state.
- Today they should be treated as metadata that documents intended relationships, not as enforced behavior.

## Source Inputs

- [src/agentic/resources/rules/INDEX.md](/Users/gorky/Projects/agentic/src/agentic/resources/rules/INDEX.md)
- [src/agentic/features/workspace_contract/sync/domain/value_object.py](/Users/gorky/Projects/agentic/src/agentic/features/workspace_contract/sync/domain/value_object.py)
- [src/agentic/features/workspace_contract/rules/domain/entity.py](/Users/gorky/Projects/agentic/src/agentic/features/workspace_contract/rules/domain/entity.py)

## Boundary

Keep this page descriptive and maintainership-focused. Governing rule content still belongs in the packaged rule tree itself, and workspace-local policy still belongs in the generated project contract.