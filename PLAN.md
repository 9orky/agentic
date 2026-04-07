# File Tree

- docs/
- docs/project/
- docs/project/getting-started.md
- docs/runtime/
- docs/runtime/workspace-contract.md
- docs/runtime/architecture-check.md
- docs/maintainers/
- docs/maintainers/rule-system.md
- docs/maintainers/packaged-resources.md
- agentic/
- agentic/agentic.yaml
- agentic/rules/
- agentic/rules/local/
- src/
- src/agentic/
- src/agentic/resources/
- src/agentic/resources/agentic.yaml
- src/agentic/resources/copilot-instructions.md
- src/agentic/resources/README.md
- src/agentic/features/
- src/agentic/features/workspace_contract/
- src/agentic/features/workspace_contract/sync/
- src/agentic/features/workspace_contract/sync/domain/value_object.py
- src/agentic/features/workspace_contract/sync/infrastructure/file_repository.py
- src/agentic/features/workspace_contract/sync/ui/views.py

# Goal

Align the runtime workspace-contract layout with the documented `agentic/rules/local/` surface and add agent-facing guidance inside the `agentic/` operating boundary so an LLM can discover how to author `agentic.yaml` as project state rather than relying on the user-facing `docs/` tree.

# Execution Frame

- The generated `agentic/` folder should contain the working contract an LLM needs inside a target repository.
- The runtime layout, sync behavior, and docs must agree on where repo-local profile artifacts live.
- `agentic/agentic.yaml` should remain durable project state, but it also needs explicit agent-facing authoring guidance near the file or in adjacent packaged operating instructions.
- Human-facing `docs/` pages remain useful reference material, but the agent should not need to infer `agentic.yaml` authoring strategy only from `docs/`.

# Phases

## Phase 01 - Domain

- Objective: define the contract model for the explicit `local/` workspace surface and the minimum agent-facing `agentic.yaml` authoring guidance that belongs inside the `agentic/` operating boundary.
- Owning layer: `domain`
- Inputs: current runtime layout model, current workspace-contract docs, current packaged `agentic.yaml`, and the current bootstrap instruction surface.
- Outputs: an approved contract for `agentic/rules/local/` as the runtime-owned local profile surface and an approved content model for agent-facing `agentic.yaml` authoring instructions.
- Acceptance: the plan makes it explicit what belongs in runtime layout, what belongs in sync behavior, and what agent-facing `agentic.yaml` guidance must be available inside the generated contract.

## Phase 02 - Infrastructure

- Objective: align the runtime layout and sync model with the explicit `local/` surface.
- Owning layer: `infrastructure`
- Inputs: approved contract decisions from Phase 01 and the current sync implementation.
- Outputs: runtime layout and repository-loading code that treat `agentic/rules/local/` as a first-class contract surface, plus sync and summary behavior that describe that surface consistently.
- Acceptance: runtime code, sync summaries, and generated contract structure all agree on `local/` without preserving stale layout terminology such as `overrides/` and `project/` as the primary model.

## Phase 03 - Application

- Objective: provide agent-facing instructions for authoring `agentic.yaml` within the generated contract surface.
- Owning layer: `application`
- Inputs: approved `local/` contract model from Phase 01 and aligned runtime surface from Phase 02.
- Outputs: packaged guidance in `agentic/`-reachable assets that tells an agent how to discover tags, boundaries, flows, exclusions, and seam exceptions when crafting `agentic.yaml`.
- Acceptance: an agent operating from the generated contract can learn how to draft or refine `agentic.yaml` without depending primarily on human-facing docs.

## Phase 04 - UI

- Objective: align the operator-facing and agent-facing explanations so the generated contract is understandable to both humans and agents.
- Owning layer: `ui`
- Inputs: completed runtime layout changes and completed agent-facing `agentic.yaml` guidance.
- Outputs: updated runtime and project docs, packaged resource references, and bootstrap messaging that point users and agents to the same contract surface with the right audience split.
- Acceptance: the docs explain the system honestly, the packaged resources expose the agent operating guidance clearly, and the generated `agentic/` folder reads as the primary LLM working surface.

# Acceptance

- The runtime workspace-contract model explicitly supports `agentic/rules/local/` as the local profile surface.
- Sync loading, summaries, and generated layout stop treating `overrides/` and `project/` as the primary local contract model.
- The generated `agentic/` folder contains agent-facing guidance for authoring `agentic.yaml`, not only human-facing explanations in `docs/`.
- `agentic/agentic.yaml` remains durable project state and gains clear adjacent guidance for discovering tags, boundaries, flow layers, and exclusions.
- Human-facing docs and packaged runtime assets describe the same contract without conflating user reference docs with the agent operating surface.

# Decisions

- The explicit `local/` runtime surface replaces `overrides/` and `project/` completely; the old surfaces should be removed rather than carried forward as the primary model.
- Agent-facing `agentic.yaml` guidance should live as a combination of inline or adjacent generated-contract guidance and bootstrap instructions, not only in human-facing docs.
- The guidance should not impose a heavy required discovery workflow; it should instead keep the agent anchored in the `agentic/` folder and the generated contract surface.

# Open Questions

- Does the `agentic/` folder need an additional dedicated guide for LLM operation beyond `copilot-instructions.md` and the rule tree, or is strengthening those existing assets enough?
