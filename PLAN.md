# File Tree

- docs/
- docs/maintainers/
- docs/runtime/
- agentic/
- agentic/rules/
- agentic/rules/local/
- agentic/rules/local/execution/
- agentic/rules/local/structure/
- src/
- src/agentic/
- src/agentic/resources/
- src/agentic/resources/rules/
- src/agentic/resources/rules/shared/
- src/agentic/resources/rules/shared/execution/
- src/agentic/resources/rules/shared/structure/

# Goal

Promote universal planning workflow and reusable layered-architecture guidance into shared rules, then reduce the local rule branch so it becomes a small, structured, machine-validatable repo profile that an agent can generate deterministically after discovery and a user can fine-tune through the local rules folder.

# Execution Frame

- The user initializes the `agentic/` folder.
- The user asks the agent to discover the repository, its architecture, and the required local narrowing.
- The agent generates structured local-rule artifacts that can be validated by machine rather than freeform prose.
- The user reviews the generated local rules in `agentic/rules/local/` and iterates on them with an agent.
- Shared rules remain the reusable baseline; local rules are the generated project-specific profile.

# Proposed Local Override Format

- Keep local overrides as markdown rule documents with strict YAML frontmatter rather than introducing a separate data format first.
- Require frontmatter fields for `scope: local`, `generated_by: agent`, `discovered_from`, `narrows_paths`, `profile_kind`, and `validation_version`.
- Restrict `profile_kind` to a small set such as `workflow`, `layers`, `module_seams`, and `starter_files`.
- Restrict `narrows_paths` to shared rule documents only so local output cannot silently fork other local output.
- Keep the body in short fixed sections so validation remains simple: `Observed Repository Facts`, `Local Decisions`, `Constraints`, and `Review Checks`.
- Require each `Local Decisions` bullet to be declarative, machine-checkable when possible, and scoped to one concern.
- Treat `Observed Repository Facts` as discovery output and `Local Decisions` as the actual narrowing so the user can review what the agent inferred versus what it decided.
- Validate the artifact by schema first, then by allowed narrowing rules, then by contradiction checks against the referenced shared rules.

# Phases

## Phase 01 - Domain

- Objective: define the shared rule semantics that become the new baseline for planning workflow and layered or onion structure, so agent-authored local overrides only need to express narrow project-specific choices discovered from the repository.
- Owning layer: `domain`
- Inputs: current shared execution and structure rules, current local execution and structure tightenings, and the agreed direction that plan artifact naming is universal while layered architecture is an optional shared mode.
- Outputs: updated shared execution rule intent for universal artifact naming and updated shared structure rule intent for generic layered or onion dependency guidance, plus a clear boundary for what local overrides are allowed to narrow after agent discovery.
- Acceptance: shared rules can describe universal planning artifacts and reusable layered dependency constraints without relying on this repository's exact layer names or Python scaffolds, and the remaining local override surface is small enough for an agent to generate consistently.

## Phase 02 - Infrastructure

- Objective: align the maintainership and runtime contract documentation with the new shared versus local split and make the agent-authored local override model explicit.
- Owning layer: `infrastructure`
- Inputs: the shared rule semantics approved in Phase 01 and the current runtime and maintainership docs.
- Outputs: documentation that describes the shared rule corpus as the home of universal workflow and optional layered structure, while local rules remain a preserved workspace overlay for narrow repo-specific agent-authored tightening structured for validation.
- Acceptance: documentation does not imply an effective-rule merge engine, describes the new split consistently, states what an agent may place in local overrides versus shared rules, makes the discovery-to-generation-to-review workflow explicit, and documents the proposed structured local override format.

## Phase 03 - Application

- Objective: shrink the local execution and structure rules to project-specific tightenings only and make those tightenings easy for an agent to emit without policy duplication.
- Owning layer: `application`
- Inputs: approved shared workflow and layered-structure guidance plus the current local branch.
- Outputs: local execution docs that drop universal artifact naming and local structure docs that keep only chosen layer names, package seams, starter-file conventions, and any other repo profile decisions an agent must state explicitly in a structured format.
- Acceptance: local rules read as a small specialization layer on top of shared rules rather than a second general rule system, an agent can author or update them without re-explaining shared policy, and the artifacts are machine-validatable against the proposed format.

## Phase 04 - UI

- Objective: align the agent-facing rule-routing surface with the reduced local branch and the promoted shared guidance so agents know when to emit a local override versus rely on shared rules.
- Owning layer: `ui`
- Inputs: approved shared and local rule documents from earlier phases.
- Outputs: updated rule indexes or adjacent agent-facing guidance, if needed, so agents are routed through shared workflow first and then into repo-specific narrowing only when necessary, with explicit guidance for discovery, structured generation, and later user-led fine-tuning in `agentic/rules/local/`.
- Acceptance: the agent-facing contract makes the new precedence readable without inventing runtime merge behavior and makes local override authoring deterministic.

# Acceptance

- Shared execution rules define universal plan artifact naming.
- Shared structure rules support layered or onion architecture as a reusable option.
- Local structure rules keep only this repository's selected layer names, Python seam conventions, starter-file expectations, and similar narrow repo profile choices.
- Local execution rules keep only repository-specific execution tightening that remains after universal workflow is promoted.
- The remaining local override surface is small and explicit enough for an agent to author reliably.
- Agent-generated local rule artifacts are structured so machine validation can reject malformed or overly broad local narrowing.
- The structured local override format separates discovered facts from narrowing decisions so user review can challenge either one independently.
- The user review loop is centered on inspecting and refining `agentic/rules/local/` after generation.
- Maintainer, runtime, and agent-facing guidance all describe the same shared versus local boundary.

# Open Questions

- Should shared structure guidance treat layered and onion as one generic inward-dependency model with alternate vocabulary, or as separate documented options?
- After universal artifact naming moves to shared execution rules, is any repo-specific naming behavior left in local execution at all?
- Should the agent-facing routing surface point to the local branch only after the shared branch is already known, or should it also name the shared-to-local precedence explicitly at the top level?
- Should agent-authored local overrides stay as full markdown rule docs, or shrink further into a smaller project-profile format that expands into docs only when needed?
- Is the proposed markdown-plus-frontmatter profile format sufficient, or should local overrides eventually move to a smaller data-first profile that renders into markdown for review?