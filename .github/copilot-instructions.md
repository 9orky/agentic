# Workspace Instructions

In this repository, `src/agentic/resources/` is the first place to inspect for rule-system prompts and packaged contract changes.

## Required First Reads

Before proposing changes, planning work, or exploring the codebase, read in this order:

1. `src/agentic/resources/rules/AGENT.md`
2. the relevant scoped core docs under `src/agentic/resources/rules/`
3. the code that owns the contract change when the task affects bootstrap, update, or handoff behavior

For architecture, module-shape, or refactor tasks, also read:

1. `src/agentic/resources/rules/FEATURE.md`
2. `src/agentic/resources/rules/MODULE.md`
3. `src/agentic/resources/rules/REFACTORING.md`

## Operating Rule

Treat `src/agentic/resources/` as the package source of truth for:

1. coding and planning rules
2. the bootstrapped project contract
3. the shared LLM handoff content
4. the packaged configuration surface

Do not start with general repository exploration until the relevant shared rule files and owning feature code have been read.

## Rule Source Of Truth

1. Documents under `src/agentic/resources/` are the global SSOT for the shared rules and bundled docs shipped by this package.
2. The bootstrapped local `agentic/` folder in a target project is a synced runtime contract, not the upstream SSOT.
3. Local core docs under `agentic/rules/*.md` are update-owned shared rails. Repo-local edits belong only under `agentic/rules/overrides/` and `agentic/rules/project-specific/`.
4. When a broadly reusable rule is discovered, update `src/agentic/resources/` first.
5. We are still building the rules by learning stable patterns. Promote reusable rules to the shared SSOT and keep repo-local clarifications in the extension folders.
6. Do not re-export a deeper boundary module through a higher feature entry point. If a feature owns both `__init__.py` and `cli.py`, keep those seams separate and import the needed seam from the correct boundary module.

## Conflict Rule

If current code structure conflicts with `agentic/` guidance:

1. treat the codebase as behavioral reference, not architectural authority
2. update `src/agentic/resources/` first if the issue reveals a reusable shared rule
3. then update the bootstrap or handoff behavior so target projects receive the right shared contract
