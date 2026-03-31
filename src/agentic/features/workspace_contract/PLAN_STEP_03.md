# Goal

Move the rule-schema audit family end to end into `rule_schema_audit`, including its owned domain concepts, markdown and rule-tree adapters, audit query and service flow, and audit presentation, while preserving feature-root behavior and any temporary `contract.*` compatibility still required by tests.

# Planned Blast Radius

Implementation Tree:
```text
src/agentic/features/workspace_contract/
  rule_schema_audit/
    __init__.py
    application/
      __init__.py
      queries/
        __init__.py
        describe_rule_schema_drift.py
      services/
        __init__.py
        rule_schema_validation/
          __init__.py
          service.py
          rule_schema_drift_finding.py
          rule_schema_validation_result.py
          rule_schema_report_builder.py
    domain/
      __init__.py
      service/
        __init__.py
        rule_schema_policy.py
      value_object/
        __init__.py
        rule_document_class.py
        rule_document_schema.py
        rule_schema_violation.py
        rule_section_requirement.py
        shared_rule_path.py
    infrastructure/
      __init__.py
      filesystem/
        __init__.py
        rule_markdown_document.py
        rule_markdown_parser.py
        rule_tree_reader.py
      resources/
        __init__.py
        packaged_rules_reader.py          # only if this ownership proves cleaner than sync ownership
    ui/
      __init__.py
      views/
        __init__.py
        rule_schema_drift_view.py
  contract/
    application/...                       # temporary re-exports for audit symbols
    domain/...                            # temporary re-exports for audit-owned concepts
    infrastructure/...                    # temporary re-exports for audit-owned adapters
    ui/...                                # temporary re-exports for audit views
  __init__.py                             # feature-root audit function remains stable
  cli.py                                  # feature-root CLI routes check-rules through audit seam
tests/
  test_workspace_contract_application.py
  test_workspace_contract_domain.py
  test_workspace_contract_infrastructure.py
  test_workspace_contract_ui.py
```

Constraints:
- Keep `describe_rule_schema_drift` and `check-rules` behavior identical, including finding codes and local-mirror semantics.
- Do not reopen sync ownership decisions from step 2 unless a real seam defect is discovered.
- If `PackagedRulesReader` remains shared, expose it through one approved seam and avoid sibling deep imports.
- Keep the feature-root error mapping unchanged.

Layer Ownership:
- Owning layer: `application`
- This is application-owned because the audit query and its result contract define the user-visible read-side seam.
- Domain, infrastructure, and UI moves are support work for that seam and must complete within this step.

Dependency Direction:
- `rule_schema_audit.ui` may depend only on `rule_schema_audit.application`.
- `rule_schema_audit.application` may depend on `rule_schema_audit.domain` and `rule_schema_audit.infrastructure`.
- Any dependency on sync-owned layout or packaged-resource access must use an exported sync seam, not a deep import.

Architectural Risk Check:
- SSOT: The risk is splitting the rule-schema result contract across old and new modules. Make `rule_schema_audit` the single owner of `RuleSchemaValidationResult` and related findings.
- DRY: Do not duplicate markdown parsing or rule-tree traversal helpers between `contract` and `rule_schema_audit`; move them intact.
- YAGNI: Do not add a generic document-analysis module.
- SOLID: Keep parsing, validation, and reporting within one audit-owned module because they change together under the current model.

Decision Log:
- `RuleSchemaValidationResult` becomes audit-owned.
- `check-rules` remains a feature-root CLI concern that delegates into the audit module.
- Temporary audit compatibility re-exports stay in place until step 4.

# Inputs

- Step 1 sibling seams
- Step 2 stable `workspace_sync` seam for any approved shared dependency
- Current audit query, services, domain concepts, infrastructure adapters, and view under `contract`

# Outputs

- `rule_schema_audit` owns the audit use-case family end to end.
- Feature-root wrappers use `rule_schema_audit` instead of `contract.application`.
- Existing `contract.*` audit imports still resolve through compatibility shims if still required.

# Scope

- Move audit-owned files into `rule_schema_audit`.
- Update imports and `__all__` surfaces for the audit family.
- Rewire feature-root audit helpers and CLI routing to the new audit seam.
- Update tests only as needed to reflect the new owning seam or documented compatibility policy.

# Out of Scope

- Further splitting audit into parsing versus validation modules.
- Removing the `contract` package.
- Changing audit result formatting or exit-code behavior.

# Domain Model Impact

- `RuleSchemaPolicy`: ownership moves to `rule_schema_audit.domain.service`.
- `RuleDocumentClass`, `RuleDocumentSchema`, `RuleSchemaViolation`, `RuleSectionRequirement`, and `SharedRulePath`: move to `rule_schema_audit.domain.value_object`.
- `RuleSchemaValidationResult`: becomes audit-owned application contract.
- Colocated `DDD.md`: unchanged; no strategic model change.

# Owning Layer

`application`

# Execution Plan

Execution Order:
- Move audit-owned domain concepts and domain shim exports.
- Move audit-owned infrastructure adapters and infrastructure shim exports.
- Move the audit query and validation/report services.
- Move the audit UI view and rewire feature-root CLI and wrappers.
- Update any remaining compatibility imports under `contract`.

Allowed Adaptations:
- Introduce one explicit imported seam from `workspace_sync` only if a shared concept still needs it.
- Update tests from deep owning imports to new sibling imports when the touched anchor is no longer intended to be primary.
- Keep audit DTO and finding class names stable even if their package path changes.

Stop And Ask If:
- The audit flow needs more than one stable dependency on `workspace_sync` internals.
- Result-shape preservation would require duplicate DTO ownership.
- A shared concept cannot be placed cleanly in either sibling module.

Implementation Notes:
- Treat this as a move-and-import-fix step.
- Keep the check-rules path read-only; no state-changing logic should drift into the audit module.
- Preserve `build_default_describe_rule_schema_drift` and related result types.

# Verification

- Run the workspace-contract test subset, especially schema-audit application, infrastructure, and UI tests.
- Run the top-level `agentic check` command if the targeted tests pass.
- Confirm the check-rules CLI path and feature-root audit function still return the same findings and exit behavior.

# Completion Criteria

- Audit-owned code lives under `rule_schema_audit`.
- The feature root works without importing audit implementations from `contract.application`.
- Any remaining `contract` audit paths are forwarding-only compatibility shims.

# Handoff Notes

- Step 4 can remove or reduce the `contract` package once both sibling modules are stable and test coverage has been updated.
- Record any remaining compatibility imports that still have external consumers.