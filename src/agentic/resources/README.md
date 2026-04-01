# Packaged Resources

`src/agentic/resources/` is the packaged source-of-truth directory for runtime data that ships with `agentic`.

## Contents

- `rules/`: packaged shared rule documents mirrored into target workspaces
- `agentic.yaml`: packaged starter architecture configuration
- `copilot-instructions.md`: packaged bootstrap instruction text
- `arch/`: extractor assets used by the architecture-check feature

## Maintainer Guidance

- Keep this tree aligned with the runtime loaders under `src/agentic/features/workspace_contract/`.
- Treat everything here as shipped package data, not as ad hoc project notes.
- Keep project-facing documentation in `docs/`, not in this packaged resources tree.
- Do not represent project-local rule policy here unless the runtime is intentionally shipping reusable defaults.

## Rules Tree

- The packaged rules tree is shared guidance only.
- Workspace-local rule additions belong in the generated project contract, not in this packaged resources tree.
- Rule-schema validation scans the packaged rules tree from here.

## Key References

- [src/agentic/features/workspace_contract/sync/infrastructure/file_repository.py](/Users/gorky/Projects/agentic/src/agentic/features/workspace_contract/sync/infrastructure/file_repository.py)
- [src/agentic/features/workspace_contract/rules/infrastructure/file_repository.py](/Users/gorky/Projects/agentic/src/agentic/features/workspace_contract/rules/infrastructure/file_repository.py)
- [src/agentic/resources/rules/INDEX.md](/Users/gorky/Projects/agentic/src/agentic/resources/rules/INDEX.md)