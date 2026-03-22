# Feature Module-First Remodel Plan

## Objective

Replace the current feature-first, layer-direct rule model with a module-first feature model where a feature owns modules and each module owns its own `domain`, `infrastructure`, `application`, and `ui` layers.

## Scope

In scope:

1. remodel the packaged rules so feature routes to module before any layer decision
2. move feature layer rule documents one level deeper under a module-specific path
3. update planning and refactoring guidance to use the new navigation path
4. update workspace-contract behavior and tests that assume `feature/layers/*`
5. refactor existing features to the approved module-first anatomy after the rule model is accepted

Out of scope:

1. changing the meaning of the four architectural layers
2. changing the generic module boundary contract unless the remodel exposes a real conflict
3. adding new business capabilities unrelated to the remodel

## Business Capability, Bounded Context, And Subdomain

- Business capability: agent-readable architecture governance for packaged rules and generated local workspace contracts
- Bounded context: rule-system navigation and feature structure governance
- Subdomain: internal design governance for how `agentic` describes and bootstraps feature anatomy

## Extracted Domain Concepts

1. Feature Anatomy Model
2. Feature Module
3. Module Layer Set
4. Rule Navigation Path
5. Workspace Contract Mirror
6. Rule Sync Policy

## Identity, Invariants, And Lifecycle Expectations

| Concept | Classification | Identity | Invariants | Lifecycle |
| --- | --- | --- | --- | --- |
| Feature Anatomy Model | policy | shared default feature shape | feature does not own layers directly; feature routes to modules first | evolves when the shared rule model changes |
| Feature Module | architectural entity | module name within one feature | one public boundary, one public seam, owns its own layer set | created when a feature needs one bounded unit of responsibility; may split later |
| Module Layer Set | value object | ordered set owned by one module | layer set is `domain -> infrastructure -> application -> ui`; layers do not float at feature root | created with a module and changes only when module shape changes |
| Rule Navigation Path | value object | resolved markdown path sequence | navigation must remain explicit and stepwise; no skipped ownership inference | changes when rule files move or split |
| Workspace Contract Mirror | entity | local `agentic/` rule tree for one project root | local mirror must match packaged shared-rule paths except approved overrides and project-specific additions | created by init, refreshed by update, validated by check |
| Rule Sync Policy | domain service | sync decision for one packaged-to-local comparison | path mapping must be deterministic and derived from packaged resources | runs during summary, update, and drift detection |

## Owning Enclosure, Public Boundary, And Public Seam

- Owning enclosure: packaged shared rules under `src/agentic/resources/rules/` and their mirrored local `agentic/rules/` tree
- Public boundary: the navigable rule tree exposed through `AGENT.md`, `FEATURE.md`, `PLANNING.md`, `REFACTORING.md`, and `MODULE.md`
- Public seam: explicit markdown links between router documents and leaf documents, plus workspace-contract APIs that enumerate packaged rule paths

## Affected Features And Owning Responsibilities

| Feature | Responsibility Affected | Owning Part |
| --- | --- | --- |
| shared packaged rules | feature navigation and layer placement | packaged rule docs in `src/agentic/resources/rules/` |
| workspace_contract | sync, summary, drift reporting, and local mirror expectations for shared rule paths | workspace-contract domain service, infrastructure resource reader, filesystem reader, and UI views/tests |
| architecture_check | no model change expected, but feature examples and guidance may need path updates if they cite shared rule navigation | feature README or tests only if they mention the old path |

## Explicit Layer Placement

| Material Concept | Owning Layer | Why |
| --- | --- | --- |
| feature-to-module routing contract | `ui` of the rule system documentation surface | it is navigation and entrypoint guidance, not domain behavior |
| module boundary contract | `application` of the rule system documentation surface | it governs orchestration of internal module shape and allowed interactions |
| per-layer ownership rules inside one module | matching target layer document | each leaf defines the owning layer's responsibilities directly |
| packaged rule-path enumeration | `infrastructure` | it reads packaged resources from the filesystem/package data |
| sync decision about create/update/preserve | `domain` | it is deterministic policy over shared rule paths |
| rendered drift and summary messages | `ui` | presentation concern only |

## Application Orchestration Required

1. update the shared rule routers so feature resolves module ownership before any layer read
2. align planning and refactoring rules to the new module-first navigation path
3. update workspace-contract expectations so packaged and local shared-rule paths enumerate the new structure without special casing legacy paths
4. migrate existing features to the approved anatomy after the rule contract is stable
5. remove first-level layer assumptions from tests, fixtures, and rendered messages

## Infrastructure Responsibilities Required

1. ship the moved markdown files as packaged data
2. keep packaged rule enumeration recursive so new nested paths are discovered automatically
3. update any tests or fixtures that hardcode `feature/layers/*`
4. ensure local mirror creation and update place the new files at the correct nested destinations

## UI Responsibilities Required

1. keep human-facing rule navigation short and explicit
2. render drift output and summaries using the new relative paths
3. avoid teaching legacy direct-to-layer navigation once the remodel lands

## Intended Dependency Direction

1. `AGENT.md` routes to `feature/FEATURE.md` or other top-level rule sets
2. `feature/FEATURE.md` routes to a feature-module router before any layer leaf
3. the feature-module router routes to one layer leaf only when module ownership is already clear
4. planning and refactoring rules may link into the module-layer leaf path, but must not inline those rules
5. workspace-contract infrastructure reads packaged paths; domain sync policy remains path-agnostic and consumes the enumerated paths only

## Concise Re-Model

Target shared-rule shape:

```text
rules/
  AGENT.md
  feature/
    FEATURE.md
    module/
      MODULE.md
      layers/
        DOMAIN.md
        INFRASTRUCTURE.md
        APPLICATION.md
        UI.md
  module/
    MODULE.md
  planning/
    PLANNING.md
    phases/
      BIG_PICTURE.md
      STEPS.md
```

Remodel rules:

1. feature owns modules, not layers
2. module owns the layer set for the responsibility being placed
3. generic `rules/module/MODULE.md` stays the reusable module boundary contract
4. `rules/feature/module/MODULE.md` becomes the feature-internal router that decides which module is in play and then routes to that module's layer leaf
5. all cross-rule references to `rules/feature/layers/*` move to `rules/feature/module/layers/*`

## Assumptions

1. the current top-level `rules/module/MODULE.md` remains valid as the generic module contract
2. one feature may contain one or more modules, but the rule system only needs to model module-first navigation, not enumerate project-specific module names
3. recursive packaged-path discovery is sufficient for the deeper folder structure and does not require a hardcoded manifest
4. existing local projects can be migrated by normal workspace-contract update flows once the new packaged paths ship

## Major Phases

### Phase 1: Rule Contract Remodel

- Input: current packaged rule tree and approved module-first target model
- Output: updated packaged rules, updated local mirrored rules in this repo, and updated navigation references

### Phase 2: Workspace Contract Alignment

- Input: approved rule-path changes from phase 1
- Output: updated sync, summary, drift detection, and tests that recognize the new nested paths

### Phase 3: Feature Refactor

- Input: accepted rule contract and passing workspace-contract behavior
- Output: existing features reorganized to module-first anatomy, starting with `workspace_contract` and then other features that still rely on first-level layers

### Phase 4: Verification And Cleanup

- Input: migrated rule docs, code, and tests
- Output: passing test suite for affected areas, no stale references to `feature/layers/*`, and updated repo memory or docs if the stable contract changed

## Acceptance Criteria

1. no shared rule router describes a feature as directly owning layers
2. all shared-rule links and rule text route layer decisions through a feature-module hop
3. workspace-contract bootstrap, sync, summary, and drift reporting operate correctly with the moved rule files
4. no tests or shipped docs rely on `feature/layers/*`
5. `workspace_contract` is refactored against the approved module-first model instead of preserving the old shape behind compatibility wording

## Known Risks And Open Questions

1. the name and role split between generic `rules/module/MODULE.md` and feature-local `rules/feature/module/MODULE.md` must stay explicit or navigation will become ambiguous
2. `workspace_contract` may need an intermediate compatibility window if local-project update expectations are stricter than current tests show
3. some README examples or schema-drift fixtures may reference the old path indirectly and will need a repo-wide sweep
4. if existing feature code is not easily partitioned into modules, the refactor may need a default single module per feature as a transitional state