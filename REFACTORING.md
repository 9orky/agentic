# Refactoring Rules

Use this document when reshaping existing code.

Do not use current structure as the design target. Use the intended design and move the code toward it.

Use it to make refactor decisions deterministic while keeping room for pragmatic internal adjustment.

Use the standard development run from `AGENT.md`.

This document specializes how the shared run behaves when existing structure must be changed.

This document is not complete by itself for ownership or boundary design.

Also read:

- `FEATURE.md` for feature ownership and public boundaries
- `MODULE.md` for module shape and public entry-point rules
- `TESTS.md` when the refactor changes verification strategy or coverage
- `PLANNING.md` when the refactor is governed by an approved plan step

Do not treat a missing rule here as permission to violate a relevant feature, module, or plan rule.

## Core Stance

1. Start from the target design, not the current structure.
2. Treat existing callers as behavioral reference only.
3. Do not assume legacy boundaries are valid boundaries.
4. Do not ship structure that is known to be wrong just because it is temporarily convenient.

## Default Workflow

1. define the target boundary first
2. write or confirm the plan
3. rebuild in a sibling `_refactor` or `_refactored` folder when the change is substantial
4. keep ownership of ports, models, services, and orchestration inside the new slice
5. stub unfinished downstream dependencies behind local adapters
6. add targeted boundary verification before caller swap
7. promote the new slice to the canonical path
8. delete the legacy slice only after the new path is active and verified

If the change is small and the current structure already matches the target boundary, an in-place refactor is acceptable. Do not create a sibling folder mechanically when it adds ceremony without architectural value.

## Refactor Execution Focus

During the shared run, focus on these refactor-specific checkpoints:

1. confirm the target boundary before editing
2. decide whether the change is in-place or a fresh slice
3. keep temporary pragmatism local and removable
4. verify against the target contract, not the legacy structure
5. update the plan or docs if the refactor changed the documented understanding

## Refactor Rules

1. Do not mutate legacy structure in place when the target design needs a fresh slice.
2. Do not introduce helper exports to preserve accidental old callers.
3. Do not collapse responsibilities into the public boundary as a shortcut.
4. Do not let a parent module assemble a child module from several internal imports when the child can own that assembly.
5. Do not import from behind another module's public entry point.
6. Do not silently merge explicit caller configuration with defaults unless the contract documents merge semantics.
7. Do not implement later-phase behavior early unless the scope explicitly changes.
8. Do not replace the target design with hardcoded branchy scaffolding just to get a temporary green result.
9. Do not turn a temporary compatibility shim into a hidden permanent boundary.

## Allowed Pragmatism

Use pragmatic adjustments when they preserve the target direction:

1. add a narrow compatibility shim that is clearly local and removable
2. keep a temporary adapter inside the owning slice
3. reorder refactor substeps when the approved outputs remain the same
4. simplify an internal tactic if it preserves boundaries and contracts

Do not confuse pragmatic internal adjustment with permission to change ownership, public contracts, or target boundaries silently.

## Verification Rules

Before accepting a refactor step, verify:

1. public behavior is covered through the intended boundary first
2. cross-module imports still go through public entry points
3. helper internals do not leak through exports
4. explicit inputs still mean what they say after normalization
5. the result still matches the approved plan

If verification fails because the plan assumed the wrong tactic but the same contract is still viable, adjust the tactic and continue. Revise the plan only when the contract, ownership, or acceptance result must change.

## Guidance

- if the task is mostly boundary design, read `FEATURE.md` and `MODULE.md` first
- if the task is mostly sequencing or rollout, read `PLANNING.md` as well
- if a refactor reveals a plan mismatch, fix the plan before changing the contract
- if a shortcut seems necessary, stop and ask before taking it
- prefer local temporary adapters over public temporary seams
- prefer reversible compatibility measures over disposable structural hacks
- if a refactor tactic is acceptable here but would violate feature or module ownership, the feature or module rule still applies
- keep the run shape stable: inspect, define target boundary, implement minimal valid slice, verify against the intended boundary