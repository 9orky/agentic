# PLAN_STEP_04

## Goal

Finalize the application-layer refactor by aligning package exports, removing obsolete loose service files, and verifying that the final application tree matches the local rules.

## Planned Blast Radius

Implementation Tree:

```text
src/agentic/features/workspace_contract/contract/application/
├── __init__.py
├── commands/
│   ├── __init__.py
│   ├── bootstrap_project.py
│   └── update_project.py
├── queries/
│   ├── __init__.py
│   ├── describe_rule_schema_drift.py
│   └── describe_workspace_contract.py
└── services/
    ├── __init__.py
    ├── workspace_contract_summary_service.py
    ├── workspace_contract_sync/
    │   ├── __init__.py
    │   ├── service.py
    │   └── sync_report_builder.py
    └── rule_schema_validation/
        ├── __init__.py
        ├── service.py
        ├── rule_schema_validation_result.py
        ├── rule_schema_drift_finding.py
        └── rule_schema_report_builder.py
```

    Constraints:

    1. keep the externally visible application seam stable
    2. do not reintroduce loose multi-file service sprawl under `services/`
    3. remove stale files that would violate the target anatomy or confuse imports
    4. final verification must confirm local-rule compliance, not only test success

    Layer Ownership:

    1. `application` owns final export shape and internal service structure
    2. `domain`, `infrastructure`, and `ui` remain unchanged except as downstream consumers of the stable application seam

    Dependency Direction:

    1. feature-boundary and UI imports continue to depend only on application public exports
    2. application public exports depend on command, query, and minimal service-boundary shims only
    3. no external code depends on removed loose service files

    Architectural Risk Check:

    1. SSOT: `application/__init__.py` and package shims remain the single public import source for application consumers.
    2. DRY: obsolete loose service files are removed instead of being left as parallel import paths or duplicate ownership surfaces.
    3. YAGNI: do not add compatibility shims or public aliases unless they are required to preserve an existing supported seam.
    4. SOLID: public seams stay narrow, internal files remain private behind package shims, and cleanup does not move responsibilities across layers.

    Decision Log:

    1. the public application seam stays stable even though the internal service topology changes
    2. obsolete service files should be removed, not retained as drift-prone leftovers

## Inputs

1. [PLAN.md](/Users/gorky/Projects/agentic/PLAN.md)
2. completed steps 01 through 03
3. current application exports, feature-boundary imports, and affected tests

## Outputs

1. final `application/__init__.py`, `commands/__init__.py`, `queries/__init__.py`, and `services/__init__.py` exports
2. removal of obsolete loose service files replaced by the new service boundaries
3. verified application-layer compliance with the local rules

## Scope

In scope:

1. `application/__init__.py`
2. `commands/__init__.py`
3. `queries/__init__.py`
4. `services/__init__.py`
5. removal of superseded loose service files under `application/services/`
6. test alignment needed to validate the final application structure and public seam

## Out of Scope

1. new behavior changes outside the application refactor
2. CLI wording changes
3. domain or infrastructure redesign

## Domain Model Impact

No domain model changes.

## Owning Layer

Application.

## Execution Plan

Execution Order:

1. align all application package export files with the target public seam
2. remove obsolete loose service modules replaced by service-folder boundaries
3. update remaining imports in the feature boundary and tests if needed
4. run targeted verification for application, feature-boundary, and UI tests
5. verify the final file tree against the local application rules

Allowed Adaptations:

1. package export order may change for clarity
2. tests may be updated to reflect new internal import paths only when the public seam is intentionally unchanged

Stop And Ask If:

1. keeping the public seam stable is impossible without adding a compatibility shim the plan did not account for
2. a removed loose service file is still required by an external consumer that should remain supported

Implementation Notes:

1. delete obsolete files instead of leaving dead compatibility clutter inside `application/services/`
2. verify both file-tree shape and public imports before closing the refactor

## Verification

1. application exports expose only the approved public seam
2. obsolete loose service files are gone
3. the final application file tree matches the approved target anatomy
4. application, feature-boundary, and relevant UI tests pass
5. local-rule compliance is satisfied for commands, queries, and services

## Completion Criteria

1. the application layer matches the target tree from [PLAN.md](/Users/gorky/Projects/agentic/PLAN.md)
2. there are no stray loose service files representing split concerns without folder boundaries
3. the feature boundary still exposes the same public application seam
4. the refactor is ready for final review against the root plan

## Handoff Notes

After this step, the application-layer refactor should be complete and ready for code-to-plan alignment review.
