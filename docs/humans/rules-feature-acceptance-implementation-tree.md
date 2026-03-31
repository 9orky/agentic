# Rules Feature Acceptance Implementation Tree

This document records the exact implementation slice that will be built to accept the new `workspace_contract.rules` feature as the canonical packaged-rule schema checker.

This is an implementation artifact, not a design brainstorm. Items below are written as committed scope for the next change set.

## Acceptance Target

The accepted feature will do one job:

- validate packaged markdown rule documents from `agentic/resources/rules`
- report schema violations and parse exceptions through the new `rules` feature
- own the canonical CLI path for rule checking

The accepted feature will not do these things in this slice:

- compare packaged rules against a local bootstrapped mirror
- preserve `rule_schema_audit` behavior inside the new feature
- add command-side state mutation logic to the new rules feature
- migrate or delete old code in the same change set as acceptance wiring

## Implementation Tree

```text
src/agentic/features/workspace_contract/
├── __init__.py                                   [edit]
├── cli.py                                        [edit]
└── rules/
    ├── __init__.py                               [edit]
    ├── application/
    │   ├── __init__.py                           [edit]
    │   └── queries.py                            [edit]
    ├── domain/
    │   ├── __init__.py                           [keep]
    │   ├── entity.py                             [keep]
    │   ├── repository.py                         [keep]
    │   ├── service.py                            [keep]
    │   └── value_object.py                       [keep]
    ├── infrastructure/
    │   ├── __init__.py                           [keep]
    │   └── file_repository.py                    [keep]
    └── ui/
        ├── __init__.py                           [edit]
        ├── cli.py                                [edit]
        └── views.py                              [edit]
```

## File-Level Implementation

### `src/agentic/features/workspace_contract/rules/domain/*`

These files are already the accepted minimum and will stay as they are:

- `entity.py` will remain the place for parsed rule document entities and markdown extraction rules.
- `value_object.py` will remain the place for rule document class, violations, section requirements, and parse errors.
- `service.py` will remain the place for `RuleSchemaPolicy`.
- `repository.py` will remain the abstract repository seam.

No additional domain classes, repositories, or services will be added in this acceptance slice.

### `src/agentic/features/workspace_contract/rules/infrastructure/*`

These files are already sufficient and will stay as they are:

- `file_repository.py` will remain the single concrete adapter that loads packaged rule documents.
- `__init__.py` will remain the simple shim that exports `file_repository`.

No second repository and no local-mirror adapter will be implemented in this acceptance slice.

### `src/agentic/features/workspace_contract/rules/application/queries.py`

This file will be edited so the application report becomes the complete source of reporting facts.

The implementation will:

- keep `build_rule_schema_report()` as the single query entry point
- keep direct usage of `file_repository` and `RuleSchemaPolicy`
- keep exception mapping for `RuleDocumentParseError`
- add summary fields onto `RuleSchemaReport`

The report DTO will carry:

- `documents`
- `documents_checked`
- `documents_with_issues`
- `has_findings`

The document DTO will continue to carry:

- `path`
- `document_class`
- `observed_section_headings`
- `has_navigation_targets`
- `violations`
- `exception`

No additional query file and no `commands.py` will be added in this acceptance slice. The feature remains query-only.

### `src/agentic/features/workspace_contract/rules/application/__init__.py`

This file will be edited to export the accepted application surface only:

- `RuleDocumentReport`
- `RuleSchemaReport`
- `RuleSchemaViolationReport`
- `build_rule_schema_report`

No command exports will be added.

### `src/agentic/features/workspace_contract/rules/ui/views.py`

This file will be edited so the view becomes rendering-only.

The implementation will:

- render application-provided summary fields instead of computing them locally
- continue to render one line per document
- continue to render parse exceptions inline
- continue to render violation details inline

The view will not perform report aggregation logic after this change.

### `src/agentic/features/workspace_contract/rules/ui/cli.py`

This file will be edited so the new UI becomes the canonical rule-checking entry point.

The implementation will:

- register `check-rules` as the canonical command name for the new rules feature
- keep `check-rule-schema` as a compatibility alias during the transition
- call `build_rule_schema_report()`
- print lines from the view
- return non-zero when `report.has_findings` is true

The command will not accept `--local-mirror` in this acceptance slice.

### `src/agentic/features/workspace_contract/rules/ui/__init__.py`

This file will be edited to export the accepted UI seam:

- the CLI registration function used by `workspace_contract.cli`
- the default report view builder
- the report view type

### `src/agentic/features/workspace_contract/rules/__init__.py`

This file will be edited to expose the accepted feature seam.

The implementation will:

- continue exporting domain types
- continue exporting the application report/query surface
- continue exporting infrastructure seam types
- expose the final UI registration seam if needed by the feature boundary

No compatibility exports for `rule_schema_audit` will be added here.

### `src/agentic/features/workspace_contract/cli.py`

This file will be edited to switch the canonical `check-rules` registration from the old audit path to the new rules UI.

The implementation will:

- remove the old `check-rules` command implementation from this file
- register the new rules CLI from `rules.ui`
- keep `init` and `update` unchanged
- stop importing the old audit application and UI for rule checking

This is the public command handoff that makes the new rules feature accepted at the CLI boundary.

### `src/agentic/features/workspace_contract/__init__.py`

This file will be edited to hand the public Python seam over to the new rules feature.

The implementation will:

- stop exporting the old rule-schema audit result/query types as the primary rule-checking seam
- export the new `rules` report/query types instead, if a public rule-checking seam is kept here
- leave bootstrap and update exports intact

This change is limited to public seam rewiring. It does not delete the old module.

## Explicit Non-Implementation List

These items will not be implemented as part of this acceptance slice:

- `src/agentic/features/workspace_contract/rules/application/commands.py`
- local mirror comparison in the new `rules` feature
- migration of old `rule_schema_audit` internals into the new feature
- deletion of `rule_schema_audit`
- deletion of legacy rules docs
- changes to workspace sync bootstrapping behavior

## Resulting Accepted Shape

After this implementation, the accepted runtime flow will be:

1. `workspace_contract.cli` registers the new `rules.ui` command as canonical `check-rules`.
2. `rules.ui.cli` invokes `build_rule_schema_report()`.
3. `rules.application.queries` loads packaged documents through `file_repository`.
4. `rules.domain.service` validates each parsed rule document.
5. `rules.ui.views` renders the application report without recalculating report state.

## Acceptance Boundary

This implementation is complete when these statements are true:

- `check-rules` runs through `src/agentic/features/workspace_contract/rules/ui/cli.py`
- the new rules feature is the canonical packaged-rule schema checker
- the application report owns summary facts
- the UI only renders
- no additional complexity from old mirror-drift behavior is pulled into the new feature