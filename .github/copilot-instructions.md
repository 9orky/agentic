# Workspace Instructions

In this repository, `agentic/` is the first place to inspect for every prompt.

## Required First Reads

Before proposing changes, planning work, or exploring the codebase, read in this order:

1. `agentic/guide/WORKFLOW.md`
2. `agentic/guide/COMMANDS.md`
3. `agentic/rules/AGENT.md`
4. `agentic/rules/project-specific/_PROJECT.md`

For architecture, module-shape, or refactor tasks, also read:

1. `agentic/reference/ARCHITECTURE_MAP.md`
2. `agentic/rules/project-specific/PACKAGE_ARCHITECTURE.md`
3. `agentic/rules/project-specific/REFACTORING_APPROACH.md`

## Operating Rule

Treat `agentic/` as the project source of truth for:

1. coding and planning rules
2. architecture direction
3. refactor approach
4. project-specific constraints for future LLM runs

Do not start with general repository exploration until the relevant `agentic/` files have been read.

## Rule Source Of Truth

1. Documents under `src/agentic/resources/` are the global SSOT for the shared rules and bundled docs shipped by this package.
2. The local `agentic/` folder is this repository's project-local contract and synced reference copy, not the upstream SSOT for shared rules.
3. When a broadly reusable rule is discovered, update `src/agentic/resources/` first and then update `agentic/` so the repo stays in sync.
4. We are still building the rules by learning and noticing durable patterns. Promote only stable reusable rules to the global SSOT; keep repo-only clarifications under `agentic/rules/project-specific/`.
5. Do not re-export a deeper boundary module through a higher feature entry point. If a feature owns both `__init__.py` and `cli.py`, keep those seams separate and import the needed seam from the correct boundary module.

## Conflict Rule

If current code structure conflicts with `agentic/` guidance:

1. treat the codebase as behavioral reference, not architectural authority
2. update `src/agentic/resources/` first if the issue reveals a reusable shared rule
3. then sync the local `agentic/` docs or place repo-specific clarifications under `agentic/rules/project-specific/`

## Current Repo-Specific Direction

1. The approved direction is feature-first clean architecture.
2. The canonical implementation lives in `src/agentic/`.
3. Do not keep completed migration scaffolding or parallel package roots once promotion is complete.
4. Backward compatibility is not a governing constraint unless the user explicitly reintroduces it.
5. Each feature owns its commands in a local `cli.py`.
6. The master `src/agentic/cli.py` binds feature-owned command sets and should not absorb feature logic.
7. Each feature owns its own internal `app/` layer, and the feature-local `cli.py` consumes that layer.
8. Keep feature public APIs minimal: expose only the primary feature seam and the minimum command-binding seam needed by the master CLI.