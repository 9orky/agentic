# Rule System

This page explains the current packaged-rule model and how it differs from workspace-local rule additions.

## Current Model

- The packaged rule corpus under `src/agentic/resources/rules/` is shared source-of-truth guidance that ships with `agentic`.
- Shared execution rules now own universal planning workflow naming such as `PLAN.md` and `PLAN_STEP_0X.md`.
- Shared structure rules now describe layered or onion architecture generically as an inward-dependency model whose concrete layer names may be narrowed by a project.
- Workspace sync mirrors those packaged rule documents into the generated project contract under `agentic/rules/`.
- The intended local surface is a small project profile under `agentic/rules/local/` that an agent generates after discovery and a user then reviews and fine-tunes.
- True workspace-local additions are preserved by the runtime, but current runtime code does not resolve packaged and local documents into an effective merged rule set.
- The packaged `src/agentic/resources/rules/local/` branch is obsolete under this model and should not remain as shipped pseudo-local guidance.

## Discovery Workflow

- The user initializes the `agentic/` folder.
- The user asks the agent to discover the repository, its architecture, and the project-specific narrowing needed beyond shared rules.
- The agent emits a small local profile under `agentic/rules/local/` rather than restating shared policy.
- The user reviews that generated local profile and fine-tunes it with an agent.
- Shared rules stay reusable and generic; local rules stay narrow and project-specific.

## Proposed Local Profile Format

- Keep the local profile as markdown rule documents with strict YAML frontmatter rather than introducing a separate data format first.
- Required frontmatter should include `scope: local`, `generated_by: agent`, `discovered_from`, `narrows_paths`, `profile_kind`, and `validation_version`.
- `profile_kind` should stay within a small controlled set such as `workflow`, `layers`, `module_seams`, and `starter_files`.
- `narrows_paths` should point only to shared rule documents so local output narrows the shared baseline instead of forking other local files.
- The markdown body should stay in fixed sections: `Observed Repository Facts`, `Local Decisions`, `Constraints`, and `Review Checks`.
- `Observed Repository Facts` captures what the agent discovered; `Local Decisions` captures the actual narrowing the project wants to keep.
- This format is the current documentation target for machine validation and user review. It is not yet a fully enforced runtime contract.

## Metadata Status

- `tightens_paths` and `escalation_paths` exist in the frontmatter model and may support future resolver behavior.
- Current runtime code does not use those fields to compute merged rule state.
- Today they should be treated as metadata that documents intended relationships, not as enforced behavior.

## Local Narrowing Boundaries

- Local profiles may choose concrete layer names, optional subsets of layers, root seam names, and starter scaffolds.
- Local profiles may document repository-specific workflow tightening that remains after shared workflow guidance is applied.
- Local profiles must not invert inward dependency direction, weaken seam-based boundaries, or restate shared rules as if they were project-specific.
- Local profiles should stay small enough that an agent can regenerate them deterministically after repository discovery.

## Source Inputs

- [src/agentic/resources/rules/INDEX.md](/Users/gorky/Projects/agentic/src/agentic/resources/rules/INDEX.md)
- [src/agentic/features/workspace_contract/sync/domain/value_object.py](/Users/gorky/Projects/agentic/src/agentic/features/workspace_contract/sync/domain/value_object.py)
- [src/agentic/features/workspace_contract/rules/domain/entity.py](/Users/gorky/Projects/agentic/src/agentic/features/workspace_contract/rules/domain/entity.py)

## Boundary

Keep this page descriptive and maintainership-focused. Governing rule content still belongs in the packaged rule tree itself, and workspace-local policy still belongs in the generated project contract. Do not describe a computed effective-rule graph unless runtime code actually implements it.