# Packaged Resources

`src/agentic/resources/` is the packaged data root for assets that ship with the installed `agentic` package.

## What Belongs Here

- `rules/`: the packaged shared rule corpus that is mirrored into a target workspace.
- `agentic.yaml`: the packaged starter architecture config.
- `copilot-instructions.md`: the packaged bootstrap instruction content.
- `arch/`: extractor assets used by the architecture-check feature.

## Runtime Consumption

- Workspace sync loads packaged rules recursively from `src/agentic/resources/rules/` through the runtime loader in [src/agentic/features/workspace/sync/infrastructure/file_repository.py](/Users/gorky/Projects/agentic/src/agentic/features/workspace/sync/infrastructure/file_repository.py).
- The sync feature also loads packaged `agentic.yaml` and `copilot-instructions.md` from the same packaged resources root.
- Rule-schema validation scans the packaged rules tree, not the human-facing docs tree under `docs/`.
- Repo-specific operating decisions still belong in the generated `agentic/` contract, especially under `agentic/rules/local/`, not in packaged resources.

## Maintainer Rules

- Treat the packaged resources tree as shipped runtime data, not as general project documentation.
- Keep file references and wording aligned with what the runtime actually enumerates and mirrors.
- Do not model project-local guidance as packaged resources unless the runtime is intentionally shipping reusable defaults.
- Keep `docs/` separate from packaged resources; project docs explain the system but do not become shipped rule assets.

## Files That Must Stay Aligned

- [src/agentic/resources/rules/INDEX.md](/Users/gorky/Projects/agentic/src/agentic/resources/rules/INDEX.md)
- [src/agentic/resources/copilot-instructions.md](/Users/gorky/Projects/agentic/src/agentic/resources/copilot-instructions.md)
- [src/agentic/resources/README.md](/Users/gorky/Projects/agentic/src/agentic/resources/README.md)
- [src/agentic/features/workspace/sync/infrastructure/file_repository.py](/Users/gorky/Projects/agentic/src/agentic/features/workspace/sync/infrastructure/file_repository.py)

## Boundary

Use this page for maintainership guidance about packaged assets. The governing shared rule content lives inside the packaged rule tree, while the generated `agentic/` folder remains the live repository contract.
