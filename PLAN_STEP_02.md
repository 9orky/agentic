# Implementation Tree

- src/
- src/agentic/
- src/agentic/features/
- src/agentic/features/workspace_contract/
- src/agentic/features/workspace_contract/sync/
- src/agentic/features/workspace_contract/sync/domain/value_object.py
- src/agentic/features/workspace_contract/sync/infrastructure/file_repository.py
- src/agentic/features/workspace_contract/sync/ui/views.py

# Goal

Align the runtime workspace-contract layout, loading, and sync summaries with `agentic/rules/local/` as the only local profile surface.

# Step Contract

- Inputs: [PLAN.md](/Users/gorky/Projects/agentic/PLAN.md) and the approved contract decisions from [PLAN_STEP_01.md](/Users/gorky/Projects/agentic/PLAN_STEP_01.md).
- Outputs: runtime layout and sync behavior that use `local/` consistently and stop presenting `overrides/` and `project/` as the primary model.
- Scope: workspace-contract runtime code and sync summary messaging.
- Out-of-scope: human-facing docs, rule routing text, and final agent-facing `agentic.yaml` guidance wording.
- Owning layer: `infrastructure`
- Dependency direction: depends only on the semantic baseline from Step 01.
- Earlier-layer dependencies: Step 01 contract decisions.
- Root seam updates: sync summaries and contract views may be updated only after the layout and repository-loading changes are coherent.

# Execution

1. Replace the layout model's old local surfaces with explicit `local/` support.
2. Update repository loading and summary reporting so they enumerate and describe `agentic/rules/local/` consistently.
3. Remove stale primary terminology around `overrides/` and `project/` from the runtime model where the new product direction has replaced it.
4. Keep runtime behavior honest about what is loaded, preserved, and generated.

# Verification

- Confirm runtime code explicitly supports `agentic/rules/local/`.
- Confirm sync summaries no longer direct users toward stale local surfaces.
- Confirm the runtime contract surface and the generated workspace shape agree.

# Completion

- Runtime code matches the new contract model.
- Phase 03 can add agent-facing `agentic.yaml` guidance against the updated generated surface.
