# Implementation Tree

- src/
- src/agentic/
- src/agentic/features/
- src/agentic/features/workspace_contract/
- src/agentic/features/workspace_contract/sync/
- src/agentic/features/workspace_contract/sync/domain/value_object.py
- src/agentic/features/workspace_contract/sync/infrastructure/file_repository.py
- agentic/
- agentic/rules/
- agentic/rules/local/
- agentic/agentic.yaml
- src/agentic/resources/
- src/agentic/resources/agentic.yaml
- src/agentic/resources/copilot-instructions.md

# Goal

Define the concrete contract for `agentic/rules/local/` as the only runtime local profile surface and define the minimum agent-facing `agentic.yaml` authoring guidance that must exist inside the generated `agentic/` boundary.

# Step Contract

- Inputs: [PLAN.md](/Users/gorky/Projects/agentic/PLAN.md), the current workspace-contract layout model, the current generated `agentic/` surface, and the current packaged `agentic.yaml` and bootstrap instruction assets.
- Outputs: approved contract decisions for the `local/` runtime surface and an approved content model for agent-facing `agentic.yaml` guidance inside the generated contract.
- Scope: contract semantics only; no runtime code or doc rewrites in this step.
- Out-of-scope: sync implementation, view changes, user-facing docs, and final packaged guidance wording.
- Owning layer: `domain`
- Dependency direction: none; this step establishes the semantic baseline for later implementation.
- Earlier-layer dependencies: none.
- Root seam updates: none.

# Execution

1. Define `agentic/rules/local/` as the sole runtime-owned local profile surface.
2. State that `overrides/` and `project/` are removed rather than retained as compatibility-first surfaces.
3. Define what agent-facing `agentic.yaml` guidance must be available inside `agentic/` so an LLM can operate from the generated contract rather than from `docs/`.
4. Define the boundary that keeps the agent anchored in the `agentic/` folder instead of spreading authoring logic across unrelated repository locations.

# Verification

- Confirm the contract names `local/` as the only local profile surface.
- Confirm the step does not preserve `overrides/` or `project/` as the primary product model.
- Confirm the approved guidance target for `agentic.yaml` is inside the generated `agentic/` operating boundary.

# Completion

- Later steps can implement runtime, guidance, and doc changes without re-deciding the contract model.
- Phase 02 can update the runtime model directly against a stable domain decision.
