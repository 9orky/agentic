# Shared Rule System Tactical Plan

## Purpose

This document defines the tactical model for the `Shared Rule System` bounded context.

It explains how the `src/agentic/resources/` implementation root expresses shared rule-document ownership, navigation structure, and packaged source-of-truth templates.

## Scope

This tactical plan governs `src/agentic/resources/`.

It covers the packaged rules tree under `src/agentic/resources/rules/`, the maintenance guidance in `src/agentic/resources/README.md`, and the packaged default templates in `src/agentic/resources/agentic.yaml` and `src/agentic/resources/copilot-instructions.md`.

It should stay aligned with the repo-level strategic model in [DDD.md](../../DDD.md).

## Model Decisions

1. The `src/agentic/resources/` root is the current implementation root for the `Shared Rule System` bounded context, so this tactical artifact uses the strategic bounded-context name as its source of truth.
2. This bounded context is modeled around immutable packaged assets and navigation semantics rather than long-lived runtime entities.
3. The `rules/` tree owns shared rule documents, router-versus-leaf structure, and navigation paths; the resource-root templates own the packaged default bootstrap instruction and starter architecture agreement.
4. `Workspace Contract` consumes these packaged assets as published language and packaged source of truth, but it does not own their meaning, taxonomy, or navigation contract.
5. No domain-owned repository contract exists today because the packaged resource tree is already the versioned source of truth and downstream consumers should enumerate it directly.

## Concept Catalog

| Concept | Classification | Identity | Invariants | Lifecycle | Owning Module | Owning Layer |
| --- | --- | --- | --- | --- | --- | --- |
| Shared rule tree | Value object and source-of-truth snapshot | Identified by one packaged directory snapshot under `src/agentic/resources/rules/` | Only managed markdown rule documents belong in the tree, and relative document paths must stay deterministic | Versioned with a package release and consumed read-only at runtime | `rules` | `resource package` |
| Rule router document | Value object | Identified by one rules-tree-relative markdown path and its navigational document class | A router must make the next valid links explicit and must not inline downstream detail that belongs in child documents | Authored with the rules tree, versioned in package data, and mirrored into managed workspaces | `rules` | `resource package` |
| Rule leaf document | Value object | Identified by one rules-tree-relative markdown path and its leaf document class | A leaf must own one concern's detailed rules without acting as a router for unrelated detail | Authored with the rules tree, versioned in package data, and mirrored into managed workspaces | `rules` | `resource package` |
| Navigation path | Value object | Identified by an ordered sequence of markdown targets from one router to the next selected document | Each hop must be explicit from the current document, and links must remain local to the governed tree | Created when rule documents are authored and consumed whenever an agent navigates the rules | `rules` | `resource package` |
| Rule-set bootstrap | Value object | Identified by the entry markdown document for one rule concern such as `AGENT.md`, `ddd/DDD.md`, or `planning/PLANNING.md` | A bootstrap must make the next routing choice legible for its concern and remain discoverable from its governing parent | Versioned with the rules tree and updated whenever a rule set is added or split | `rules` | `resource package` |
| Rules-maintenance policy | Policy | One maintenance policy expressed through `src/agentic/resources/README.md` | Router documents own discovery, leaf documents own detail, and new rule sets must be discoverable from the governing router | Refined as the rules tree evolves and consumed during rule-authoring work | `resources` | `resource package` |
| Packaged bootstrap instruction template | Value object | Identified by the packaged file path `src/agentic/resources/copilot-instructions.md` | The template must stay a minimal pointer to the local `agentic/` directory and must not embed rule detail inline | Versioned in package data and copied into managed workspaces during bootstrap or update | `resources` | `resource package` |
| Packaged architecture-agreement template | Value object | Identified by the packaged file path `src/agentic/resources/agentic.yaml` | The template must remain a valid starter architecture agreement and exclude the local `agentic/` tree from analysis by default | Versioned in package data and copied into managed workspaces during bootstrap or update | `resources` | `resource package` |

## Aggregate And Repository Decisions

1. No dedicated entity is modeled in this bounded context today.
2. No aggregate boundary is modeled today because the bounded context is expressed as versioned immutable packaged assets rather than a mutable runtime consistency boundary.
3. No domain-owned repository contract exists today because downstream consumers should enumerate the packaged source-of-truth tree directly instead of loading it through a duplicate repository abstraction.
4. If the bounded context later gains mutable authoring workflows, independent publication state, or a richer lifecycle around rule-set versions, revisit aggregate and repository decisions before introducing a repository or aggregate ad hoc.

## Open Questions

1. Should rule-document metadata such as document class and navigation targets eventually become first-class code-owned value objects inside this bounded context rather than being inferred only by downstream consumers?
2. Should the `Shared Rule System` move into a first-class feature boundary if rule authoring grows beyond packaged assets and maintenance guidance?
3. Should the packaged default templates remain in this bounded context permanently, or should they split into a separate template-publication context if their lifecycle diverges from the rule tree?