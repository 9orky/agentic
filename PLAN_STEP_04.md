# Implementation Tree

- docs/
- docs/project/
- docs/project/getting-started.md
- docs/runtime/
- docs/runtime/workspace-contract.md
- docs/runtime/architecture-check.md
- docs/maintainers/
- docs/maintainers/rule-system.md
- docs/maintainers/packaged-resources.md
- src/
- src/agentic/
- src/agentic/resources/
- src/agentic/resources/README.md

# Goal

Align human-facing and packaged explanations so the generated `agentic/` folder is clearly the primary LLM operating surface while `docs/` remains the human-facing reference surface.

# Step Contract

- Inputs: [PLAN.md](/Users/gorky/Projects/agentic/PLAN.md), the runtime layout changes from [PLAN_STEP_02.md](/Users/gorky/Projects/agentic/PLAN_STEP_02.md), and the agent-facing `agentic.yaml` guidance from [PLAN_STEP_03.md](/Users/gorky/Projects/agentic/PLAN_STEP_03.md).
- Outputs: updated project, runtime, and maintainer docs plus packaged resource references that describe the same contract and audience split.
- Scope: explanatory docs and packaged resource descriptions.
- Out-of-scope: further runtime code changes or new contract surfaces beyond what earlier steps approved.
- Owning layer: `ui`
- Dependency direction: depends only on completed earlier steps and must not redefine their semantics.
- Earlier-layer dependencies: Steps 01, 02, and 03.
- Root seam updates: update operator-facing entrypoints and packaged resource descriptions only after the runtime and agent-facing assets are stable.

# Execution

1. Update runtime and project docs so they point to `agentic/` as the primary LLM operating boundary.
2. Remove or replace stale references to `overrides/` and `project/` where the product direction has eliminated them.
3. Explain the audience split clearly: `agentic/` for live operating contract, `docs/` for human-facing reference.
4. Keep packaged resource references aligned with what the runtime actually loads and what the agent actually reads.

# Verification

- Confirm docs and packaged references describe the same contract surface.
- Confirm the generated `agentic/` folder is presented as the main LLM working surface.
- Confirm stale local-surface terminology is removed or clearly deprecated.

# Completion

- The runtime surface, packaged guidance, and human-facing docs are aligned.
- The four-step plan is fully expanded into executable steps with the user's decisions baked in.