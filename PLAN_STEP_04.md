# Implementation Tree

- agentic/
- agentic/rules/
- agentic/rules/INDEX.md
- agentic/rules/local/
- agentic/rules/local/INDEX.md
- src/
- src/agentic/
- src/agentic/resources/
- src/agentic/resources/rules/
- src/agentic/resources/rules/INDEX.md
- src/agentic/resources/rules/shared/
- src/agentic/resources/rules/shared/INDEX.md

# Goal

Align the agent-facing routing surface so agents discover shared workflow first, generate narrow structured local overrides only when needed, and hand the resulting local profile back for user fine-tuning.

# Step Contract

- Inputs: [PLAN.md](PLAN.md), the shared-rule baseline from [PLAN_STEP_01.md](PLAN_STEP_01.md), the docs contract from [PLAN_STEP_02.md](PLAN_STEP_02.md), and the reduced local branch from [PLAN_STEP_03.md](PLAN_STEP_03.md).
- Outputs: updated agent-facing indexes or adjacent routing guidance that make the shared-to-local precedence and local generation workflow explicit.
- Scope: routing and agent guidance only.
- Out-of-scope: further semantic rule changes, new validation code, or additional local rule content.
- Owning layer: `ui`
- Dependency direction: depends only on completed earlier steps and must not redefine their semantics.
- Earlier-layer dependencies: Steps 01, 02, and 03.
- Root seam updates: update rule-routing entrypoints and adjacent guidance only after earlier step outputs are stable.

# Execution

1. Update top-level routing so shared rules remain the baseline entrypoint.
2. Make the conditions for entering the local branch explicit: discovery complete, shared branch known, repo-specific narrowing required.
3. State that local outputs are structured agent-generated artifacts intended for later user review and fine-tuning.
4. Keep routing guidance declarative and avoid implying a runtime merge engine if one does not exist.

# Verification

- Confirm the routing surface makes shared-to-local precedence readable.
- Confirm the local branch is presented as generated project-specific profile content rather than parallel shared policy.
- Confirm root routing changes do not bypass the approved semantics established in earlier steps.

# Completion

- Agent-facing routing matches the final shared-plus-local model.
- The plan is fully expanded into executable steps without reordering or semantic drift.