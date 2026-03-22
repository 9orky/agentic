# PLAN_STEP_01

## Goal

Remodel the shared rule contract from feature-direct layers to feature-first module routing.

## Inputs

1. Approved high-level plan in `PLAN.md`
2. Existing packaged rule tree under `src/agentic/resources/rules/`
3. Existing local mirrored rule tree under `agentic/rules/`

## Outputs

1. `feature/FEATURE.md` routes to `feature/module/MODULE.md`
2. Layer leaves live under `feature/module/layers/`
3. Obsolete `feature/layers/` rule documents are removed

## Scope

Packaged shared rules, mirrored local rules, and cross-rule navigation references.

## Out of Scope

1. Feature code refactors
2. Local architecture config changes
3. Test or runtime changes outside rule-path alignment

## Constraints

1. Keep packaged rules as the shared source of truth
2. Mirror the same shape into the local `agentic/rules/` tree
3. Keep navigation explicit and module-first

## Domain Model Impact

1. Change `Feature Anatomy Model` from direct feature layers to feature-owned modules
2. Add explicit `Feature Module` router as the first structural owner below the feature boundary
3. Keep `Module Layer Set` unchanged but move it under the owning module

## Owning Layer

`ui`

## Layer Ownership

This step is owned by the rule-system documentation surface because it changes navigation, entrypoint guidance, and placement discovery rather than executable runtime behavior.

## Dependency Direction

1. `AGENT.md -> feature/FEATURE.md`
2. `feature/FEATURE.md -> feature/module/MODULE.md`
3. `feature/module/MODULE.md -> feature/module/layers/*`

## Execution Order

1. Update packaged rule routers
2. Add module router and relocated layer leaves
3. Update local mirrored rules
4. Remove obsolete direct feature-layer docs

## Allowed Adaptations

1. Tighten wording to keep routing explicit
2. Remove obsolete files when the new path fully replaces them

## Stop And Ask If

1. A second valid feature anatomy appears and cannot be represented as a local override
2. Rule navigation becomes ambiguous between generic module rules and feature-local module rules

## Implementation Notes

1. The shared source of truth remained `src/agentic/resources/rules/`
2. The local mirror was updated in lockstep to keep the repo-local contract aligned
3. Rule references moved from `feature/layers/*` to `feature/module/layers/*`

## Detailed Implementation Tree

1. Update `src/agentic/resources/rules/AGENT.md`
2. Update `src/agentic/resources/rules/feature/FEATURE.md`
3. Add `src/agentic/resources/rules/feature/module/MODULE.md`
4. Add `src/agentic/resources/rules/feature/module/layers/{DOMAIN,INFRASTRUCTURE,APPLICATION,UI}.md`
5. Update planning and refactoring cross-links
6. Mirror the same tree under `agentic/rules/`
7. Delete `src/agentic/resources/rules/feature/layers/*`
8. Delete `agentic/rules/feature/layers/*`

## Decision Log

1. Kept `rules/module/MODULE.md` as the generic module contract
2. Introduced `rules/feature/module/MODULE.md` as the feature-local module router
3. Removed direct feature-layer routing to avoid two competing anatomies

## Verification

1. Shared rule links no longer point at `feature/layers/*`
2. Packaged and mirrored trees expose the same module-first path
3. `agentic check` remained green after the rule change sequence

## Completion Criteria

1. The feature bootstrap routes to a module router
2. Layer leaves sit only under `feature/module/layers/`
3. No obsolete direct feature-layer docs remain in packaged or mirrored trees

## Handoff Notes

Step 02 must align workspace-contract expectations and tests to the new rule paths.

## Files Tree

```text
PLAN.md
PLAN_STEP_01.md
src/agentic/resources/rules/
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
agentic/rules/
  feature/
    FEATURE.md
    module/
      MODULE.md
      layers/
        DOMAIN.md
        INFRASTRUCTURE.md
        APPLICATION.md
        UI.md
```