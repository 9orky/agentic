# Goal

Collapse the old broad `contract` module into a minimal transitional compatibility surface or remove it entirely, align tests with the approved sibling seams, and perform the final structural verification for the `workspace_contract` feature.

# Planned Blast Radius

Implementation Tree:
```text
src/agentic/features/workspace_contract/
  __init__.py
  cli.py
  workspace_sync/
    __init__.py
    application/__init__.py
    domain/__init__.py
    infrastructure/__init__.py
    ui/__init__.py
  rule_schema_audit/
    __init__.py
    application/__init__.py
    domain/__init__.py
    infrastructure/__init__.py
    ui/__init__.py
  contract/
    __init__.py                            # remove if no external need remains; otherwise keep minimal shim only
    application/__init__.py                # same rule
    domain/__init__.py                     # same rule
    infrastructure/__init__.py             # same rule
    ui/__init__.py                         # same rule
tests/
  test_workspace_contract_application.py
  test_workspace_contract_domain.py
  test_workspace_contract_infrastructure.py
  test_workspace_contract_ui.py
  test_bootstrap.py
```

Constraints:
- Keep the feature-root Python API and CLI surface unchanged.
- Remove only compatibility that is no longer justified by test or external consumer needs.
- Do not leave `contract` as a second owner of behavior.
- End with clear sibling-module ownership and no deep sibling imports.

Layer Ownership:
- Owning layer: `ui`
- This is UI-owned because the final step verifies and preserves the external delivery seams while collapsing obsolete internal routing.
- Application and lower-layer edits in this step must be limited to removing forwarding paths and tightening imports after the owning modules are already stable.

Dependency Direction:
- Feature root depends on sibling module seams only.
- Tests should prefer feature-root seams or the sibling-module owning seams, not the obsolete broad `contract` internals.
- No remaining import should traverse from one sibling into another sibling's internal layer files.

Architectural Risk Check:
- SSOT: The main risk is leaving two live internal ownership paths after the split. Remove or minimize `contract` so ownership is singular.
- DRY: Do not keep duplicate test coverage for both old and new internal paths unless the compatibility window is explicitly retained.
- YAGNI: Do not preserve `contract` indefinitely just because it is convenient in local tests.
- SOLID: The final structure should make each sibling module responsible for one use-case family and keep the feature root as the only cross-module delivery seam.

Decision Log:
- Prefer deleting broad compatibility shims once tests and callers are aligned.
- If compatibility remains, it must be explicitly transitional and forwarding-only.
- Final verification includes both structural imports and behavior checks.

# Inputs

- Stable `workspace_sync` module from step 2
- Stable `rule_schema_audit` module from step 3
- Remaining `contract.*` compatibility imports and tests still depending on them

# Outputs

- Final feature anatomy matches the approved high-level plan.
- The obsolete broad `contract` owner is removed or reduced to a tiny documented shim.
- Tests and imports align with the new sibling-module ownership.

# Scope

- Remove or reduce `contract` compatibility shims.
- Update tests to assert the new owning seams.
- Run final alignment checks across code, plan, and step files.

# Out of Scope

- Additional module splits beyond `workspace_sync` and `rule_schema_audit`.
- Behavioral changes to sync or audit flows.
- Renaming the feature root or CLI commands.

# Domain Model Impact

- No concept behavior changes.
- Ownership becomes explicit in final import paths and surviving shims only.
- Colocated `DDD.md`: unchanged; no strategic model change.

# Owning Layer

`ui`

# Execution Plan

Execution Order:
- Inventory remaining `contract.*` imports in code and tests.
- Update tests and feature-root or sibling imports to the final approved seams.
- Remove or minimize obsolete compatibility shims.
- Run final alignment and behavior verification.

Allowed Adaptations:
- Keep a tiny forwarding `contract/__init__.py` only if an external caller still requires it.
- Update plan step notes if the verified final state keeps a narrowly scoped compatibility shim.
- Tighten `__all__` exports to match the final owning seams.

Stop And Ask If:
- External callers outside the current repo still rely on deep `contract.*` imports and cannot be migrated now.
- Removing `contract` would break a documented public compatibility promise.
- Final verification exposes a dependency cycle between the sibling modules.

Implementation Notes:
- Prefer the smallest final compatibility surface possible.
- The repo tests are allowed to stop importing `contract.*` directly.
- Finish with a final plan-to-code alignment check and update step notes if the approved final state differs in a still-acceptable way.

# Verification

- Run the full workspace-contract test subset.
- Run `agentic check` for end-to-end structural validation.
- Confirm feature-root Python imports and CLI registration still behave exactly as before.
- Confirm no deep sibling-import violations remain.

# Completion Criteria

- `workspace_sync` and `rule_schema_audit` are the clear internal owners.
- `contract` is removed or reduced to a minimal documented compatibility shim.
- Tests, code, and planning artifacts all agree on the final shape.

# Handoff Notes

- After this step, the feature should be ready for normal maintenance under the new module anatomy.
- Any retained compatibility shim should have an explicit removal follow-up if it is not intended to be permanent.