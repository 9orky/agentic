# Domain-Driven Design

## Purpose

This document is the strategic domain-model source of truth for the `agentic` repository.

It defines the business language, subdomains, bounded contexts, and context relationships that planning, implementation, and refactoring should preserve.

## Scope

This artifact governs repo-level strategic modeling for the repository.

When a repo-level `PLAN.md` exists, this artifact should guide its strategic domain model.

It does not replace executable planning or step execution artifacts when those plan files exist.

It also does not replace bounded-context tactical plans. Each code-facing bounded context should keep its own `TACTICAL.md` artifact near its implementation root.

When a narrower initiative needs a more specific strategic model, that initiative may create its own colocated `DDD.md` beside its owning plan artifacts, but this file remains the repo-level default.

## Ubiquitous Language

| Term | Meaning |
| --- | --- |
| Agentic | The system for deterministic cooperation between humans and coding agents through explicit, navigable project contracts. |
| Workspace contract | The managed project-local contract rooted at `agentic/`, including shared rules, local extensions, and bootstrap config. |
| Shared rules | The packaged source-of-truth rules tree shipped from `src/agentic/resources/rules/`. |
| Local mirror | The bootstrapped copy of the shared rules inside a target project's `agentic/rules/` tree. |
| Local extensions | Project-specific guidance under `agentic/rules/overrides/` and `agentic/rules/project-specific/`. |
| Bootstrap instruction | The minimal `.github/copilot-instructions.md` file that points the agent to the local `agentic/` folder. |
| Architecture agreement | The `agentic.yaml` or `agentic.yml` configuration that declares dependency rules and flow rules for architecture checking. |
| Architecture check | The validation process that reads the architecture agreement and compares it with extracted dependency structure. |
| Rule schema drift | A mismatch between the packaged shared-rule source of truth and a managed local mirror document. |
| Public seam | The exact import or document boundary intended for stable external consumption. |
| Layer shim | The explicit module boundary used for allowed cross-layer access. |
| Anchor shim | The explicit boundary used for allowed access to a domain anchor or similar owned internal structure. |
| Bounded context | A semantic boundary inside which a term has one authoritative meaning. |
| Context map | The explicit relationship model between bounded contexts. |

## Subdomains

| Subdomain | Type | Reasoning |
| --- | --- | --- |
| Agent collaboration contract | Core | This is the product's central value: making agent work inspectable, repeatable, and constrained by explicit project contracts. |
| Workspace contract management | Supporting | This subdomain bootstraps and synchronizes the local contract that enables the core collaboration model. |
| Architecture agreement validation | Supporting | This subdomain verifies that code dependencies conform to the declared architecture agreement. |
| Shared rule-system authoring | Supporting | This subdomain maintains the navigable rules tree that guides humans and agents through the collaboration contract. |

## Bounded Contexts

The code-facing tactical artifacts in this repository are organized per bounded context. Today, `workspace_contract` and `architecture_check` each act as the implementation root for one bounded context, so their `TACTICAL.md` files should reuse the strategic bounded-context names rather than only the feature names.

### Agent Collaboration Contract

Purpose:
The repo's overarching product meaning: a deterministic cooperation surface between humans and coding agents.

Core concepts:
1. contract
2. navigation
3. public seam
4. inspectability
5. repeatability

Current representation:
1. top-level product framing in [README.md](README.md)
2. strategic guidance encoded in this file
3. shared rule-system structure and bootstrap conventions

Tactical plan:
No separate tactical-plan artifact yet. This context is still expressed primarily as a repo-level strategic umbrella.

### Workspace Contract

Purpose:
Manage the project-local `agentic/` contract: bootstrap it, refresh it, describe it, and validate shared-rule drift.

Core concepts:
1. workspace contract
2. shared rule
3. local mirror
4. local extension
5. sync action
6. schema drift

Current representation:
1. `src/agentic/features/workspace_contract/` as the feature implementation root for the `Workspace Contract` bounded context
2. the generated `agentic/` folder in a target project

Tactical plan:
1. [src/agentic/features/workspace_contract/TACTICAL.md](src/agentic/features/workspace_contract/TACTICAL.md)

### Architecture Agreement Validation

Purpose:
Interpret an architecture agreement and detect dependency violations against extracted code structure.

Core concepts:
1. architecture agreement
2. boundary rule
3. flow rule
4. tag
5. analyzer
6. violation

Current representation:
1. `src/agentic/features/architecture_check/` as the feature implementation root for the `Architecture Agreement Validation` bounded context
2. the `agentic check` command surface

Tactical plan:
1. [src/agentic/features/architecture_check/TACTICAL.md](src/agentic/features/architecture_check/TACTICAL.md)

### Shared Rule System

Purpose:
Author and package a navigable rules tree that agents can follow incrementally instead of loading one flat instruction dump.

Core concepts:
1. router document
2. leaf document
3. rule set
4. navigation path
5. packaged source of truth
6. local mirror

Current representation:
1. `src/agentic/resources/` as the packaged-resource implementation root for the `Shared Rule System` bounded context
2. `src/agentic/resources/README.md`

Tactical plan:
1. [src/agentic/resources/TACTICAL.md](src/agentic/resources/TACTICAL.md)

## Context Map

| Upstream Context | Relationship | Downstream Context | Notes |
| --- | --- | --- | --- |
| Shared Rule System | Published language | Workspace Contract | Workspace contract distributes the packaged rule language into the local mirror and checks mirror drift against the packaged source of truth. |
| Shared Rule System | Published language | Agent Collaboration Contract | The product-level collaboration model depends on the rule tree being navigable, minimal, and explicit. |
| Workspace Contract | Customer-supplier | Architecture Agreement Validation | Workspace contract provisions the local contract location and default architecture config file that architecture validation consumes. |
| Agent Collaboration Contract | Upstream strategic model | Shared Rule System | The shared rules are one implementation of the broader collaboration-contract concept and must remain aligned with its language. |
| Agent Collaboration Contract | Upstream strategic model | Workspace Contract | Workspace contract is the concrete project-local manifestation of the collaboration contract. |
| Agent Collaboration Contract | Upstream strategic model | Architecture Agreement Validation | Architecture validation is one enforcement mechanism that makes the collaboration contract inspectable. |

## Boundary Rules

1. `Workspace Contract` owns bootstrapping, refresh, summary, and rule-schema drift concepts for the local `agentic/` tree.
2. `Architecture Agreement Validation` owns the meaning of boundaries, tags, flow analyzers, extracted dependencies, and violations.
3. `Shared Rule System` owns the meaning and structure of router documents, leaf documents, rule-set discovery, and packaged-rule navigation.
4. `Agent Collaboration Contract` owns the repo-level product language that explains why these bounded contexts exist and how they contribute to deterministic agent collaboration.
5. When one context consumes another context's concept, it should reuse the published upstream term rather than inventing a synonym.
6. If a feature begins to redefine another context's core term, that is a context-boundary warning and should trigger a strategic review.
7. Planning and refactoring should prefer explicit context names over vague labels such as `core`, `shared`, or `utils`.

## Open Questions

1. Should `Agent Collaboration Contract` remain only a repo-level strategic context, or should it later gain its own explicit feature boundary in code?
2. Should `Shared Rule System` eventually become a first-class feature with its own public seam, rather than living only as packaged resources plus maintenance guidance?
3. Should the packaged default templates remain in the `Shared Rule System` bounded context permanently, or should they split if their lifecycle diverges from the rule tree?