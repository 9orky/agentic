# PLAN_STEP_03

## Goal

Refactor the existing features to a module-first internal anatomy while preserving their feature-root public seams.

## Inputs

1. Stable module-first shared rule contract
2. Passing workspace-contract alignment from `PLAN_STEP_02.md`
3. Existing feature roots for `workspace_contract` and `architecture_check`

## Outputs

1. `workspace_contract` internals live under `contract/`
2. `architecture_check` internals live under `checker/`
3. Feature-root `__init__.py` and `cli.py` remain the public boundary

## Scope

Feature-internal restructuring for `workspace_contract` and `architecture_check`, plus direct internal-test import paths.

## Out of Scope

1. Shared rule wording cleanup
2. Repo-local architecture config cleanup
3. New feature modules beyond the two refactored features

## Constraints

1. Preserve feature-root public APIs
2. Do not leave first-level layer packages active as compatibility shims
3. Update direct internal tests to the new module paths

## Domain Model Impact

1. `Feature Module` becomes concrete in runtime code through `workspace_contract/contract/`
2. `Feature Module` becomes concrete in runtime code through `architecture_check/checker/`
3. `Module Layer Set` remains the same but is re-homed one level deeper under each feature

## Owning Layer

`application`

## Layer Ownership

This step is owned by application because it preserves the feature public seam and re-homes the internal layers under one module boundary per feature.

## Dependency Direction

1. Feature root imports from the internal module root
2. Internal layer dependencies remain inward according to each feature anatomy
3. Tests that intentionally reach internals import through `contract.*` or `checker.*`

## Execution Order

1. Move `workspace_contract` layer packages under `contract/`
2. Repoint the feature root and internal tests
3. Move `architecture_check` layer packages under `checker/`
4. Repoint the feature root and internal tests
5. Run both feature-specific test subsets and then the full suite

## Allowed Adaptations

1. Add internal module package markers such as `contract/__init__.py` and `checker/__init__.py`
2. Trim package-root re-exports if they introduce circular imports

## Stop And Ask If

1. Preserving the feature-root public seam becomes impossible without compatibility shims
2. A feature clearly needs more than one internal module rather than a single transition module

## Implementation Notes

1. `workspace_contract/contract/__init__.py` was reduced to a minimal internal package marker to avoid cycles
2. `architecture_check/checker/__init__.py` stayed a minimal internal package marker from the start

## Detailed Implementation Tree

1. Move `src/agentic/features/workspace_contract/{application,domain,infrastructure,ui}` to `src/agentic/features/workspace_contract/contract/`
2. Update `src/agentic/features/workspace_contract/{__init__.py,cli.py}`
3. Update workspace-contract direct internal tests
4. Move `src/agentic/features/architecture_check/{application,domain,infrastructure,ui}` to `src/agentic/features/architecture_check/checker/`
5. Update `src/agentic/features/architecture_check/{__init__.py,cli.py}`
6. Update architecture-check direct internal tests and patch paths

## Decision Log

1. Used one internal module per feature as the smallest module-first transition
2. Preserved public seams at the feature root rather than widening or duplicating exports

## Verification

1. Workspace-contract subset passed after the restructure
2. Architecture-check subset passed after the restructure
3. Full test suite passed after both features were refactored

## Completion Criteria

1. The two refactored features are module-first internally
2. Feature-root public seams still work
3. No tests or runtime imports rely on the old first-level layer packages

## Handoff Notes

Step 04 completes final verification, local contract cleanup, and shared-rule agnosticity hardening.

## Files Tree

```text
PLAN.md
PLAN_STEP_03.md
src/agentic/features/
  workspace_contract/
    __init__.py
    cli.py
    contract/
      application/
      domain/
      infrastructure/
      ui/
  architecture_check/
    __init__.py
    cli.py
    checker/
      application/
      domain/
      infrastructure/
      ui/
tests/
  test_workspace_contract_*.py
  test_architecture_*.py
  test_checker.py
```