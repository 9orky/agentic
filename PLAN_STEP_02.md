# PLAN_STEP_02

## Goal

Extract workspace-summary orchestration into a dedicated application service so `DescribeWorkspaceContract` becomes a thin query seam.

## Planned Blast Radius

Implementation Tree:

```text
src/agentic/features/workspace_contract/contract/application/
├── queries/
│   └── describe_workspace_contract.py
│       └── class DescribeWorkspaceContract
│           ├── __init__(...)
│           └── execute(project_root: Path) -> WorkspaceContractSummary
└── services/
    ├── __init__.py
    └── workspace_contract_summary_service.py
        └── class WorkspaceContractSummaryService
            ├── __init__(...)
            └── describe(project_root: Path) -> WorkspaceContractSummary
```

Constraints:

1. keep one query class in `describe_workspace_contract.py`
2. query accepts only `project_root: Path`
3. query does not assemble the workspace summary itself
4. keep this service in single-file form unless the concern unexpectedly requires extra owned internals

Layer Ownership:

1. `application` owns query delegation and summary orchestration
2. `domain` owns `WorkspaceContractSummary`
3. `infrastructure` owns workspace reads and path access
4. `ui` remains unchanged in this step

Dependency Direction:

1. `DescribeWorkspaceContract` depends on `WorkspaceContractSummaryService`
2. the summary service depends on domain policy and infrastructure readers
3. the query does not depend on command files or other services directly

Architectural Risk Check:

1. SSOT: `WorkspaceContractSummaryService` becomes the single owner of workspace-summary assembly.
2. DRY: the query stops carrying summary orchestration logic that can otherwise be duplicated elsewhere.
3. YAGNI: do not introduce a service folder, helper DTOs, or additional abstractions unless the single-file service proves insufficient.
4. SOLID: the query delegates only, the service orchestrates reads, and the domain summary stays domain-owned.

Decision Log:

1. keep the summary concern as a single-file service unless the implementation proves otherwise
2. preserve the existing query class name and return type

## Inputs

1. [PLAN.md](/Users/gorky/Projects/agentic/PLAN.md)
2. current `DescribeWorkspaceContract` query implementation
3. current `WorkspaceContractSummary` domain type and existing readers and policies

## Outputs

1. one thin `DescribeWorkspaceContract` query file
2. one `WorkspaceContractSummaryService` service file
3. preserved `WorkspaceContractSummary` return type

## Scope

In scope:

1. `queries/describe_workspace_contract.py`
2. `services/workspace_contract_summary_service.py`
3. `services/__init__.py`
4. application exports affected by the new summary service dependency

## Out of Scope

1. sync commands and sync service internals
2. rule-schema validation refactor
3. UI rendering changes

## Domain Model Impact

No domain model changes.

`WorkspaceContractSummary` remains domain-owned and is only assembled through application orchestration.

## Owning Layer

Application.

## Execution Plan

Execution Order:

1. create `WorkspaceContractSummaryService`
2. move summary assembly logic into the service
3. rewrite `DescribeWorkspaceContract` as thin delegation
4. align service exports and affected tests

Allowed Adaptations:

1. constructor dependencies may move from the query into the service
2. service method naming may be `describe(...)` or `build_summary(...)` if the behavior remains explicit

Stop And Ask If:

1. summary assembly requires additional DTOs or helpers that would force a multi-file service boundary
2. a domain type needs to move layers to complete the extraction

Implementation Notes:

1. use `WorkspaceContractSummaryService.describe(project_root: Path) -> WorkspaceContractSummary`
2. keep the query file limited to dependency setup and one delegation call

## Verification

1. `DescribeWorkspaceContract` contains one query class only
2. the query method delegates instead of orchestrating reads directly
3. the returned value remains `WorkspaceContractSummary`
4. existing application and feature-boundary summary tests still pass after updates

## Completion Criteria

1. summary orchestration lives in `WorkspaceContractSummaryService`
2. the summary query is thin and parameter-simple
3. no other application concern is refactored in this step

## Handoff Notes

This step establishes the single-file service pattern for simpler application orchestration concerns.
