# PLAN_STEP_01

## Goal

Extract bootstrap and update orchestration into one application service boundary so `BootstrapProject` and `UpdateProject` become thin command seams and `UpdateProject` no longer relies on class inheritance.

## Planned Blast Radius

Implementation Tree:

```text
src/agentic/features/workspace_contract/contract/application/
├── commands/
│   ├── bootstrap_project.py
│   │   └── class BootstrapProject
│   │       ├── __init__(...)
│   │       └── execute(project_root: Path) -> dict[str, object]
│   └── update_project.py
│       └── class UpdateProject
│           ├── __init__(...)
│           └── execute(project_root: Path) -> dict[str, object]
└── services/
    ├── __init__.py
    └── workspace_contract_sync/
        ├── __init__.py
        │   └── exports WorkspaceContractSyncService
        ├── service.py
        │   └── class WorkspaceContractSyncService
        │       ├── __init__(...)
        │       ├── bootstrap(project_root: Path) -> dict[str, object]
        │       ├── update(project_root: Path) -> dict[str, object]
        │       └── _sync_project(project_root: Path, *, overwrite_existing_shared_docs: bool) -> tuple[...]
        └── sync_report_builder.py
            └── class SyncReportBuilder
                └── build_sync_result(...) -> dict[str, object]
```

Constraints:

1. keep one command class per command file
2. commands accept only simple parameters
3. commands do not contain orchestration logic
4. update behavior must use composition, not inheritance
5. keep the returned sync payload shape stable
6. the new service folder must expose only the minimal public API needed by commands

Layer Ownership:

1. `application` owns the new sync orchestration service and thin command seams
2. `domain` remains the owner of `SyncPolicy` and layout semantics
3. `infrastructure` remains the owner of readers, writers, and packaged-rule access
4. `ui` remains unchanged in this step

Dependency Direction:

1. commands depend on the new sync service boundary
2. the sync service depends on domain policy and infrastructure collaborators
3. the sync service may depend on an internal report-builder helper inside its own folder
4. no application file in this step may depend on query files

Architectural Risk Check:

1. SSOT: `WorkspaceContractSyncService` becomes the only owner of sync orchestration; command files stop carrying their own orchestration path.
2. DRY: bootstrap and update share one orchestration path instead of duplicating sync logic across two command classes.
3. YAGNI: do not introduce new boundary DTOs, extra service layers, or new feature seams in this step.
4. SOLID: commands stay single-purpose delegators, the service owns coordination, and existing infrastructure collaborators remain separate dependencies.

Decision Log:

1. use one shared sync service instead of duplicated command orchestration
2. use folder form because the sync concern spans multiple files and two commands
3. preserve the external command names and returned payload shape

## Inputs

1. [PLAN.md](/Users/gorky/Projects/agentic/PLAN.md)
2. current command files under `src/agentic/features/workspace_contract/contract/application/commands/`
3. current `SyncReportBuilder` under `src/agentic/features/workspace_contract/contract/application/services/`

## Outputs

1. one `workspace_contract_sync/` service folder with a minimal public API
2. thin `BootstrapProject` and `UpdateProject` command classes
3. preserved sync result shape for the feature boundary and existing tests

## Scope

In scope:

1. `commands/bootstrap_project.py`
2. `commands/update_project.py`
3. `services/workspace_contract_sync/`
4. `services/__init__.py`
5. application imports affected by the new sync service boundary

## Out of Scope

1. `DescribeWorkspaceContract`
2. `DescribeRuleSchemaDrift`
3. rule-schema DTO relocation
4. UI rendering changes

## Domain Model Impact

No domain concepts are added or changed.

`SyncPolicy` remains domain-owned and is only consumed by the new application service.

## Owning Layer

Application.

## Execution Plan

Execution Order:

1. create the `workspace_contract_sync/` service folder and shim
2. move sync orchestration from `BootstrapProject` into `WorkspaceContractSyncService`
3. move sync report shaping behind the same service boundary
4. rewrite `BootstrapProject` to delegate only
5. rewrite `UpdateProject` to delegate only, without inheriting from `BootstrapProject`
6. align application imports and tests with the new internal boundary

Allowed Adaptations:

1. keep the existing helper name `SyncReportBuilder` if no rename is necessary
2. constructor dependency injection may be reshaped to fit the new service boundary
3. private helper method names may change if the public command seam stays stable

Stop And Ask If:

1. removing inheritance from `UpdateProject` would force a public API break outside `application`
2. sync result shaping turns out to be shared outside the sync service boundary in a way that needs a broader boundary decision
3. infrastructure or domain changes appear necessary to complete the extraction cleanly

Implementation Notes:

1. use `WorkspaceContractSyncService` as the single orchestration entrypoint with separate `bootstrap(...)` and `update(...)` methods
2. keep all filesystem and packaged-resource behavior delegated to existing collaborators
3. preserve the current returned dict shape consumed by the feature boundary

## Verification

1. command files contain only one class each
2. `UpdateProject` no longer subclasses `BootstrapProject`
3. both commands delegate to `WorkspaceContractSyncService`
4. existing sync application tests still pass after updates
5. application imports still expose `BootstrapProject` and `UpdateProject`

## Completion Criteria

1. the sync concern lives behind `services/workspace_contract_sync/`
2. bootstrap and update command files are thin
3. composition replaces inheritance for update behavior
4. no query or UI changes are required to finish this step

## Handoff Notes

This step establishes the service-folder pattern used later for rule-schema validation.
