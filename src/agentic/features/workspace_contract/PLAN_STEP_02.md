# Goal

Move the sync family end to end into `workspace_sync`, including its owned domain concepts, concrete adapters, commands, queries, services, and sync presentation, while preserving feature-root behavior and temporary `contract.*` compatibility.

# Planned Blast Radius

Implementation Tree:
```text
src/agentic/features/workspace_contract/
  workspace_sync/
    __init__.py
    application/
      __init__.py
      commands/
        __init__.py
        bootstrap_project.py
        update_project.py
      queries/
        __init__.py
        describe_workspace_contract.py
      services/
        __init__.py
        workspace_contract_sync/
          __init__.py
          service.py
          sync_report_builder.py
        workspace_contract_summary_service.py
    domain/
      __init__.py
      service/
        __init__.py
        sync_policy.py
      value_object/
        __init__.py
        sync_action.py
        sync_change.py
        workspace_contract_layout.py
        workspace_contract_summary.py
    infrastructure/
      __init__.py
      filesystem/
        __init__.py
        workspace_reader.py
        workspace_writer.py
      resources/
        __init__.py
        packaged_rules_reader.py          # stays here if layout ownership requires it
    ui/
      __init__.py
      views/
        __init__.py
        sync_summary_view.py
      services/
        __init__.py
        project_path_presenter.py
  contract/
    application/...                       # temporary re-exports for sync symbols
    domain/...                            # temporary re-exports for sync-owned concepts
    infrastructure/...                    # temporary re-exports for sync-owned adapters
    ui/...                                # temporary re-exports for sync views/helpers
  __init__.py                             # feature-root sync functions remain stable
  cli.py                                  # feature-root CLI still delegates through feature seam
tests/
  test_workspace_contract_application.py
  test_workspace_contract_domain.py
  test_workspace_contract_infrastructure.py
  test_workspace_contract_ui.py
  test_bootstrap.py
```

Constraints:
- Keep `init`, `update`, and `describe_workspace_contract` behavior identical.
- Do not move rule-schema audit files in this step.
- Keep `contract.*` import paths working through forwarding shims for the sync-owned symbols still referenced by tests.
- If `PackagedRulesReader` is needed by both siblings, expose it through the chosen owner seam instead of deep imports.

Layer Ownership:
- Owning layer: `application`
- This is application-owned because the migrated command and query seams define the end-to-end sync use-case surface.
- Domain, infrastructure, and UI moves in this step are subordinate re-homing for the sync use-case family and must finish in the same step.

Dependency Direction:
- `workspace_sync.ui` may depend only on `workspace_sync.application`.
- `workspace_sync.application` may depend on `workspace_sync.domain` and `workspace_sync.infrastructure`.
- `rule_schema_audit` must not import deep sync internals; if it needs layout or packaged rules later, it uses `workspace_sync` exports only.

Architectural Risk Check:
- SSOT: The risk is leaving duplicate factories in both `contract.application` and `workspace_sync.application`. Make `workspace_sync` the owner and turn `contract` into forwarding exports only.
- DRY: Do not copy sync report building or summary logic; move it intact.
- YAGNI: Do not split summary into a third inspection module.
- SOLID: Keep the sync family together so bootstrap, update, and summary continue to change for the same reason.

Decision Log:
- `describe_workspace_contract` stays with `workspace_sync`.
- The feature root continues to wrap sync command failures as `BootstrapError`.
- Temporary `contract` compatibility remains until step 4.

# Inputs

- Step 1 sibling seams and ownership decisions
- Current sync commands, query, services, domain concepts, and views under `contract`
- Current sync-related tests and feature-root wrappers

# Outputs

- `workspace_sync` owns the sync use-case family end to end.
- Feature-root wrappers use `workspace_sync` instead of `contract.application`.
- Existing `contract.*` sync imports still resolve through compatibility shims.

# Scope

- Move sync-owned files into `workspace_sync`.
- Update imports and `__all__` surfaces for the sync family.
- Rewire feature-root helpers and CLI composition to the new sync seam where relevant.
- Update tests only as needed to reflect the new owning seam or compatibility policy.

# Out of Scope

- Moving schema-audit commands, queries, services, or views.
- Removing `contract` compatibility imports.
- Changing user-facing CLI text or sync result payload shape.

# Domain Model Impact

- `SyncPolicy`: ownership moves to `workspace_sync.domain.service`.
- `WorkspaceContractLayout`: ownership follows the decision from step 1.
- `WorkspaceContractSummary`, `SyncAction`, and `SyncChange`: move to `workspace_sync.domain.value_object`.
- Colocated `DDD.md`: unchanged; no strategic model change.

# Owning Layer

`application`

# Execution Plan

Execution Order:
- Move sync-owned domain concepts and domain shim exports.
- Move sync-owned infrastructure adapters and infrastructure shim exports.
- Move sync application commands, query, and services.
- Move sync UI views and service helpers.
- Rewire feature-root wrappers and any `contract` forwarding imports.

Allowed Adaptations:
- Introduce narrow forwarding imports in `contract.*` and feature-root shims.
- Update tests from owning paths to sibling paths when the compatibility window is intentionally closed for a touched anchor.
- Add a sibling root export if another internal caller needs one stable sync seam.

Stop And Ask If:
- The schema-audit path depends on sync internals beyond the approved shared seam.
- A moved sync file appears to contain rule-schema audit behavior that cannot be separated mechanically.
- Keeping `contract.*` imports alive would require logic duplication instead of forwarding.

Implementation Notes:
- Treat this as a move-and-import-fix step, not a rewrite.
- Preserve factory names such as `build_default_bootstrap_project` and `build_default_update_project`.
- Keep sync presentation in `workspace_sync.ui`; do not leave it under the old `contract.ui` owner.

# Verification

- Run the workspace-contract test subset, especially bootstrap/update and sync presentation tests.
- Run the top-level `agentic check` command if the targeted tests pass.
- Confirm feature-root imports and current CLI commands still behave the same.

# Completion Criteria

- Sync-owned code lives under `workspace_sync`.
- The feature root works without importing sync implementations from `contract.application`.
- Any remaining `contract` sync paths are forwarding-only compatibility shims.

# Handoff Notes

- Step 3 can now move the audit family independently, with sync already reduced to a stable sibling seam.
- Record any unavoidable shared seam introduced here so step 3 does not deep-import sync internals.