# Goal

Establish the target sibling-module seams for `workspace_sync` and `rule_schema_audit`, decide the ownership of shared concepts such as `WorkspaceContractLayout`, and introduce only the compatibility shims needed to let later file moves stay mechanical.

# Planned Blast Radius

Implementation Tree:
```text
src/agentic/features/workspace_contract/
  PLAN.md
  PLAN_STEP_01.md
  __init__.py                              # keep feature-root API stable
  cli.py                                   # keep feature-root CLI shim stable
  workspace_sync/
    __init__.py                            # new module seam only
    application/__init__.py                # new application shim only
    domain/__init__.py                     # new domain shim only
    infrastructure/__init__.py             # new infrastructure shim only
    ui/__init__.py                         # new UI shim only
  rule_schema_audit/
    __init__.py                            # new module seam only
    application/__init__.py                # new application shim only
    domain/__init__.py                     # new domain shim only
    infrastructure/__init__.py             # new infrastructure shim only
    ui/__init__.py                         # new UI shim only
  contract/
    __init__.py                            # temporary compatibility anchor retained
    application/__init__.py                # temporary re-export shim retained
    domain/__init__.py                     # temporary re-export shim retained
    infrastructure/__init__.py             # temporary re-export shim retained
    ui/__init__.py                         # temporary re-export shim retained
```

Constraints:
- Do not move behavior-bearing files in this step.
- Restrict changes to seam definition, ownership decisions, and temporary re-export shims.
- Decide whether `WorkspaceContractLayout` remains owned by `workspace_sync` with an exported seam consumed by `rule_schema_audit`, or remains temporarily re-exported through `contract.domain` until later steps finish.
- Do not introduce a third sibling module or a shared-kernel package.

Layer Ownership:
- Owning layer: `application`
- This step is application-owned because it defines the composition and import seams that later end-to-end moves will use.
- Domain and infrastructure files may gain shim exports, but no domain logic or adapter behavior changes are allowed.

Dependency Direction:
- `workspace_contract` feature root may depend on `workspace_sync` and `rule_schema_audit` module seams.
- `contract` may temporarily re-export from new sibling module seams, but sibling modules must not depend on `contract`.
- New sibling `ui` shims may depend only on their sibling `application` shims.

Architectural Risk Check:
- SSOT: The risk is duplicating factory exports across feature root, `contract`, and new sibling seams. Keep one owning export per use-case family and use temporary re-exports only as pass-through shims.
- DRY: Do not copy command or query builders into the new modules yet. Only create empty or forwarding shims.
- YAGNI: No extra shared package, adapter facade, or reporting seam is allowed in this step.
- SOLID: The goal is to separate reasons to change by naming the seams now; avoid creating a new orchestration hub that keeps the old broad ownership intact.

Decision Log:
- Preserve the feature-root API from the first step onward.
- Use temporary `contract.*` re-exports to de-risk the move sequence.
- Lock the ownership decision for `WorkspaceContractLayout` before file moves begin.

# Inputs

- Approved high-level plan in `PLAN.md`
- Current `workspace_contract` feature-root exports and CLI shim
- Current internal `contract` module shims

# Outputs

- New sibling-module root packages exist with explicit shim files.
- Temporary compatibility direction is documented in code through forwarding exports only.
- Shared-concept ownership is fixed for the rest of the migration.

# Scope

- Create the empty or forwarding root/module/layer shims for `workspace_sync` and `rule_schema_audit`.
- Update feature-root and `contract` package shims only as needed to point at the future sibling seams.
- Record the ownership decision for `WorkspaceContractLayout` and any other shared value objects.

# Out of Scope

- Moving commands, queries, services, views, or concrete adapters.
- Renaming CLI commands or changing return shapes.
- Removing the `contract` package.

# Domain Model Impact

- `Workspace Contract Sync`: unchanged concept, new future module seam named.
- `Rule Schema Audit`: unchanged concept, new future module seam named.
- `WorkspaceContractLayout`: ownership decision becomes explicit in code shims.
- Colocated `DDD.md`: unchanged; no strategic model change.

# Owning Layer

`application`

# Execution Plan

Execution Order:
- Create sibling module root packages and layer shims.
- Adjust feature-root exports to prefer sibling seams where possible.
- Retain `contract` as a temporary forwarding anchor.
- Verify import graphs before any behavior-bearing move starts.

Allowed Adaptations:
- Add forwarding imports and `__all__` lists.
- Add minimal docstrings describing temporary compatibility only if needed for clarity.
- Keep unresolved sibling content behind imports that will be satisfied in later steps only if the shim itself remains import-safe.

Stop And Ask If:
- A shared concept appears to require a genuine third module.
- The feature root cannot remain stable without behavioral duplication.
- Any test or caller depends on side effects from importing a deep `contract.*` module.

Implementation Notes:
- Favor sibling-module roots as the new public seams inside the feature.
- Keep all current behavior-bearing implementations in place until step 2 or step 3.
- Make `contract` a compatibility direction, not an owning module.

# Verification

- Import the feature root and confirm its public symbols still resolve.
- Import each new sibling root and layer shim to confirm there are no circular-import failures.
- Run the workspace-contract test subset that exercises imports and public surfaces.

# Completion Criteria

- `workspace_sync` and `rule_schema_audit` exist as importable sibling modules.
- `contract` remains importable but no longer defines future ownership.
- The ownership of `WorkspaceContractLayout` is explicit enough to guide later moves.

# Handoff Notes

- Step 2 may now move sync files mechanically into `workspace_sync` without inventing new seams during the move.
- Step 3 must follow the same seam pattern for `rule_schema_audit`.