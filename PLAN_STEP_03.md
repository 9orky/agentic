# Implementation Tree

- agentic/
- agentic/agentic.yaml
- src/
- src/agentic/
- src/agentic/resources/
- src/agentic/resources/agentic.yaml
- src/agentic/resources/copilot-instructions.md
- src/agentic/resources/README.md

# Goal

Add agent-facing guidance for crafting `agentic.yaml` inside the generated `agentic/` contract so an LLM can discover how to author tags, boundaries, flow rules, and exclusions without relying mainly on human-facing docs.

# Step Contract

- Inputs: [PLAN.md](/Users/gorky/Projects/agentic/PLAN.md) and the aligned runtime surface from [PLAN_STEP_02.md](/Users/gorky/Projects/agentic/PLAN_STEP_02.md).
- Outputs: packaged and generated `agentic/`-reachable guidance that teaches an agent how to draft or refine `agentic.yaml` while staying anchored in the `agentic/` folder.
- Scope: `agentic.yaml` guidance content and nearby packaged operating instructions.
- Out-of-scope: broad user-facing docs rewrites, architecture-check engine changes, and additional routing-system redesign.
- Owning layer: `application`
- Dependency direction: depends only on the stable generated-contract surface from Step 02.
- Earlier-layer dependencies: Step 02 runtime layout alignment.
- Root seam updates: update packaged starter assets and bootstrap instructions only after the runtime contract surface is stable.

# Execution

1. Add or strengthen agent-facing authoring guidance adjacent to `agentic.yaml`.
2. Explain how to derive tags, boundary rules, flow layers, exclusions, and narrow exceptions from project structure.
3. Keep the guidance inside the `agentic/` operating boundary so an agent starts there rather than spreading discovery logic across unrelated docs.
4. Avoid imposing a heavy mandatory workflow; prefer compact operating rules that keep the agent anchored in the generated contract.

# Verification

- Confirm an agent can learn how to draft `agentic.yaml` from assets available inside the generated contract.
- Confirm the guidance stays focused on authoring durable project state rather than temporary prompt advice.
- Confirm the guidance keeps the agent anchored in `agentic/`.

# Completion

- The generated contract now contains agent-facing `agentic.yaml` authoring guidance.
- Phase 04 can align human-facing explanations with the new runtime and packaged surface.
