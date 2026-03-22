# PLAN_STEP_02

## Goal

Align workspace-contract path discovery, drift reporting, and tests with the new module-first rule paths.

## Inputs

1. Completed rule-path remodel from `PLAN_STEP_01.md`
2. Workspace-contract packaged-rule enumeration and local-mirror validation behavior

## Outputs

1. Workspace-contract tests expect `feature/module/layers/*`
2. Drift reporting and path assertions reflect the moved rule documents
3. Workspace-contract validation remains green

## Scope

Workspace-contract tests, path assertions, and rule-path validation behavior.

## Out of Scope

1. Feature-internal module refactors
2. Shared rule wording cleanup beyond path alignment
3. Architecture-check feature changes

## Constraints

1. Do not introduce a hardcoded manifest of packaged rule paths
2. Preserve recursive packaged rule enumeration
3. Keep the local mirror contract deterministic

## Domain Model Impact

1. `Rule Navigation Path` updates to the new nested locations
2. `Workspace Contract Mirror` remains the local entity that mirrors packaged rule paths
3. `Rule Sync Policy` continues to consume discovered paths rather than static lists

## Owning Layer

`infrastructure`

## Layer Ownership

This step is owned by infrastructure because it validates packaged resources, local mirror materialization, and path-discovery behavior.

## Dependency Direction

1. Packaged rule enumeration feeds workspace-contract readers
2. Sync and drift reporting consume discovered relative paths
3. Tests assert reported paths rather than redefining packaging logic

## Execution Order

1. Update workspace-contract tests to the new relative paths
2. Verify no runtime path manifest changes are required
3. Run the workspace-contract subset

## Allowed Adaptations

1. Update path assertions and fixtures
2. Keep runtime code unchanged when recursive discovery already covers the new tree

## Stop And Ask If

1. Packaged path discovery stops being recursive
2. Local mirror behavior requires a compatibility window that conflicts with current drift reporting

## Implementation Notes

1. Runtime enumeration already discovered nested paths correctly
2. The necessary changes were in test expectations and drift-path assertions

## Detailed Implementation Tree

1. Update `tests/test_workspace_contract_application.py`
2. Update `tests/test_workspace_contract_infrastructure.py`
3. Update `tests/test_workspace_contract_ui.py`
4. Re-run the workspace-contract subset

## Decision Log

1. Kept recursive path discovery as the runtime source of truth
2. Avoided path-specific code changes where tests alone were stale

## Verification

1. Workspace-contract subset passed after the path updates
2. Old `feature/layers/*` assertions were removed from workspace-contract tests

## Completion Criteria

1. Workspace-contract path assertions use `feature/module/layers/*`
2. Drift output references the moved files correctly
3. Workspace-contract tests pass

## Handoff Notes

Step 03 can refactor features internally because the shared rule path contract is now stable.

## Files Tree

```text
PLAN.md
PLAN_STEP_02.md
tests/
  test_workspace_contract_application.py
  test_workspace_contract_infrastructure.py
  test_workspace_contract_ui.py
src/agentic/features/workspace_contract/
  contract/
    infrastructure/
      resources/
        packaged_rules_reader.py
```