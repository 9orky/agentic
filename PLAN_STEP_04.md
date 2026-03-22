# PLAN_STEP_04

## Goal

Run final alignment cleanup: update the local contract, purge remaining tech-colored wording from shared rules, add an agnosticity guard, and verify the finished state.

## Inputs

1. Completed feature refactors from `PLAN_STEP_03.md`
2. Current local `agentic/agentic.yaml`
3. Current packaged shared rule docs and mirrored local rule docs

## Outputs

1. Local architecture config reflects module-first feature anatomy
2. Shared rule wording avoids named delivery or execution technologies
3. Automated tests guard stack and delivery-technology agnosticity
4. Full suite and live `agentic check` pass on the final state

## Scope

Shared rule wording cleanup, local architecture agreement cleanup, agnosticity regression tests, and final verification.

## Out of Scope

1. Additional feature refactors
2. New runtime capabilities
3. Changes to the generic packaged default config outside the repo-local contract

## Constraints

1. Keep packaged rules and mirrored local rules aligned
2. Make the agnosticity guard strict enough to catch named stacks and delivery/execution technologies without flagging common English words
3. Validate both tests and live `agentic check`

## Domain Model Impact

1. `Rule Navigation Path` remains stable while wording is tightened
2. `Workspace Contract Mirror` stays aligned with the module-first repo contract
3. `Feature Anatomy Model` now has explicit regression coverage against future tech-specific drift

## Owning Layer

`infrastructure`

## Layer Ownership

This step is owned by infrastructure because it finalizes the materialized repo-local contract, validation assets, and packaged-resource verification.

## Dependency Direction

1. Shared rule docs remain the packaged source of truth
2. The local `agentic/agentic.yaml` contract validates the actual repo shape
3. Infrastructure tests assert the packaged rule docs remain agnostic over time

## Execution Order

1. Update the local architecture config to the new module-first paths
2. Add and tighten the agnosticity guard in infrastructure tests
3. Remove remaining tech-colored rule wording in packaged and mirrored docs
4. Re-run targeted tests, full tests, and `agentic check`

## Allowed Adaptations

1. Tighten denylist terms when they are unambiguous
2. Remove ambiguous denylist terms that create false positives
3. Rephrase rule text to preserve meaning while removing named technologies

## Stop And Ask If

1. The local contract requires a different feature anatomy than the shared default
2. A wording cleanup would change the actual owning responsibilities rather than just neutralize phrasing

## Implementation Notes

1. The local `agentic/agentic.yaml` originally still pointed at first-level feature layers and produced false-negative checks
2. The agnosticity guard was expanded carefully to avoid false positives such as ordinary English words

## Detailed Implementation Tree

1. Update `agentic/agentic.yaml`
2. Update `src/agentic/resources/README.md`
3. Update packaged and mirrored infrastructure and UI rule leaves
4. Update `tests/test_workspace_contract_infrastructure.py`
5. Run targeted infrastructure tests
6. Run full test suite
7. Run `agentic check`

## Decision Log

1. Kept the packaged default config separate from the repo-local contract cleanup
2. Treated `cli`, `endpoint`, `subprocess`, `filesystem`, and `network` as cleanup targets in shared rules

## Verification

1. The agnosticity guard passed after cleanup
2. The full test suite passed
3. Live `agentic check` passed with the updated local contract

## Completion Criteria

1. Shared rules stay language- and delivery-technology agnostic
2. The repo-local contract matches the module-first code structure
3. Full verification passes without violations

## Handoff Notes

This step closes the implementation and verification work. The remaining state is a completed remodel plus formal step artifacts.

## Files Tree

```text
PLAN.md
PLAN_STEP_04.md
agentic/
  agentic.yaml
  rules/
    feature/module/layers/
      INFRASTRUCTURE.md
      UI.md
src/agentic/resources/
  README.md
  rules/
    feature/module/layers/
      INFRASTRUCTURE.md
      UI.md
    refactoring/
      REFACTORING.md
tests/
  test_workspace_contract_infrastructure.py
```