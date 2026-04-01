# Workspace Contract

The workspace contract is the generated project surface that `agentic` writes into a target repository.

## Generated Files And Folders

- `agentic/agentic.yaml`: the starter architecture agreement file
- `agentic/rules/`: mirrored packaged shared rule documents
- `.github/copilot-instructions.md`: bootstrap instruction content used for agent guidance

The layout is defined by [src/agentic/features/workspace_contract/sync/domain/value_object.py](/Users/gorky/Projects/agentic/src/agentic/features/workspace_contract/sync/domain/value_object.py).

## Shared Versus Workspace-Owned Content

The current runtime model is intentionally split:

- packaged shared rule documents come from `src/agentic/resources/rules/`
- workspace-local additions belong in `agentic/rules/overrides/` and `agentic/rules/project/`

Current runtime code preserves those workspace-local additions. It does not compute a merged effective-rule set from packaged and local rule documents.

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