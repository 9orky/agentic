# Workspace Contract

The workspace contract is the generated project surface that `agentic` writes into a target repository.

## Generated Files And Folders

- `agentic/agentic.yaml`: the starter architecture agreement file
- `agentic/rules/`: mirrored packaged shared rule documents
- `.github/copilot-instructions.md`: bootstrap instruction content used for agent guidance

The layout is defined by [src/agentic/features/workspace_contract/sync/domain/value_object.py](/Users/gorky/Projects/agentic/src/agentic/features/workspace_contract/sync/domain/value_object.py).

## Discovery And Review Workflow

- The user initializes the project-local contract with `agentic init`.
- The agent reads the shared rule baseline from `agentic/rules/` and discovers the repository-specific narrowing it needs.
- The agent writes a small local profile under `agentic/rules/local/` for later review instead of duplicating shared rule content.
- The user reviews and fine-tunes the generated local profile with an agent.
- The runtime still treats those local files as workspace-owned content; it does not compute a merged effective-rule view.

## Shared Versus Workspace-Owned Content

The current runtime model is intentionally split:

- packaged shared rule documents come from `src/agentic/resources/rules/`
- those shared documents now include universal planning workflow naming and generic layered or onion dependency guidance
- workspace-local additions are the project-specific profile the agent generates and the user tunes under `agentic/rules/local/`

Current runtime code preserves those workspace-local additions. It does not compute a merged effective-rule set from packaged and local rule documents.

## Proposed Local Profile Format

The current documentation target for local profile artifacts is:

- markdown documents with strict YAML frontmatter
- required frontmatter keys including `scope: local`, `generated_by: agent`, `discovered_from`, `narrows_paths`, `profile_kind`, and `validation_version`
- a small set of allowed `profile_kind` values such as `workflow`, `layers`, `module_seams`, and `starter_files`
- fixed markdown sections: `Observed Repository Facts`, `Local Decisions`, `Constraints`, and `Review Checks`

This format is intended to make agent output reviewable by a human and checkable by a machine. The current runtime documents that target, but does not yet enforce it as a separate stable product feature.

## Sync Behavior

`agentic init` creates the project-local contract.

`agentic update` refreshes packaged shared assets while preserving existing local workspace files.

The current sync summary reports:

- created files
- updated shared files
- preserved existing files

## Important Limits

- The runtime mirrors packaged shared documents; it does not resolve local policy into a computed rule graph.
- The code can summarize contract state internally, but there is not yet a separate user-facing command that presents that state as a stable product feature.
- The runtime preserves local profile files, but this documentation should not imply that all proposed local-profile validation is already enforced in code.
- The workspace contract and the human-facing `docs/` tree are different surfaces and should not be conflated.

## Related Docs

- [architecture-check.md](/Users/gorky/Projects/agentic/docs/runtime/architecture-check.md) for architecture validation behavior
- [../maintainers/rule-system.md](/Users/gorky/Projects/agentic/docs/maintainers/rule-system.md) for maintainership details about packaged rules versus workspace-local additions

## Source Inputs

- [src/agentic/features/workspace_contract/sync/domain/value_object.py](/Users/gorky/Projects/agentic/src/agentic/features/workspace_contract/sync/domain/value_object.py)
- [src/agentic/features/workspace_contract/sync/infrastructure/file_repository.py](/Users/gorky/Projects/agentic/src/agentic/features/workspace_contract/sync/infrastructure/file_repository.py)
- [src/agentic/features/workspace_contract/sync/ui/cli.py](/Users/gorky/Projects/agentic/src/agentic/features/workspace_contract/sync/ui/cli.py)

## Boundary

Explain runtime behavior honestly. Do not imply merged effective-rule resolution that the current toolchain does not implement.