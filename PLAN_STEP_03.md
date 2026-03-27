# PLAN_STEP_03

## Goal

Move rule-schema validation orchestration and its application-owned DTOs behind one multi-file service boundary so `DescribeRuleSchemaDrift` becomes a thin query seam and the local application rules are satisfied.

## Planned Blast Radius

Implementation Tree:

```text
src/agentic/features/workspace_contract/contract/application/
├── __init__.py
├── queries/
│   └── describe_rule_schema_drift.py
│       └── class DescribeRuleSchemaDrift
│           ├── __init__(...)
│           └── execute(project_root: Path, *, include_local_mirror: bool = True) -> RuleSchemaValidationResult
└── services/
    ├── __init__.py
    └── rule_schema_validation/
        ├── __init__.py
        │   └── exports RuleSchemaValidationService, RuleSchemaValidationResult
        ├── service.py
        │   └── class RuleSchemaValidationService
        │       ├── __init__(...)
        │       ├── describe(project_root: Path, *, include_local_mirror: bool = True) -> RuleSchemaValidationResult
        │       ├── _validate_packaged_documents(...) -> tuple[RuleSchemaDriftFinding, ...]
        │       ├── _validate_local_documents(...) -> tuple[RuleSchemaDriftFinding, ...]
        │       └── internal parsing and drift helper methods
        ├── rule_schema_validation_result.py
        │   └── class RuleSchemaValidationResult
        ├── rule_schema_drift_finding.py
        │   └── class RuleSchemaDriftFinding
        └── rule_schema_report_builder.py
            └── class RuleSchemaReportBuilder
```

Constraints:

1. keep one query class in `describe_rule_schema_drift.py`
2. query accepts only simple parameters: `project_root: Path` and `include_local_mirror: bool`
3. query does not perform validation orchestration itself
4. the multi-file rule-schema validation concern must live in its own folder with a minimal public API
5. only the necessary public result types should be exported beyond the service boundary

Layer Ownership:

1. `application` owns validation orchestration and validation result DTOs
2. `domain` owns validation policy and rule-document class semantics
3. `infrastructure` owns parsing, packaged-rule reading, rule-tree enumeration, and workspace reading
4. `ui` remains a consumer of the public validation result only

Dependency Direction:

1. `DescribeRuleSchemaDrift` depends on the `rule_schema_validation` service boundary
2. `RuleSchemaValidationService` depends on domain policy and infrastructure collaborators
3. `RuleSchemaValidationResult` and `RuleSchemaDriftFinding` are created inside the service boundary and exported minimally
4. no other command or query depends on internal files inside `rule_schema_validation/`

Architectural Risk Check:

1. SSOT: the `rule_schema_validation/` folder becomes the single owner of validation orchestration, result shaping, and public validation DTOs.
2. DRY: the query stops owning validation logic, and loose sibling DTO/helper files stop representing one concern across multiple root-level modules.
3. YAGNI: do not expose new public types beyond the current public result import and the minimum folder shim needed by consumers.
4. SOLID: the query delegates, the service orchestrates, DTOs carry data only, and domain and infrastructure responsibilities stay unchanged.

Decision Log:

1. use folder form because this concern already spans orchestration plus multiple owned DTOs and helpers
2. keep the public API minimal: service plus public result type
3. preserve the current query class name and public result behavior

## Inputs

1. [PLAN.md](/Users/gorky/Projects/agentic/PLAN.md)
2. current `DescribeRuleSchemaDrift` query implementation
3. current rule-schema service and DTO files under `application/services/`

## Outputs

1. one `rule_schema_validation/` service folder with a minimal public API
2. thin `DescribeRuleSchemaDrift` query delegation
3. relocated `RuleSchemaValidationResult` and `RuleSchemaDriftFinding` behind the service boundary

## Scope

In scope:

1. `queries/describe_rule_schema_drift.py`
2. `services/rule_schema_validation/`
3. `services/__init__.py`
4. `application/__init__.py`
5. test imports affected by relocated DTO definitions

## Out of Scope

1. sync-service behavior
2. summary-query behavior
3. UI message wording changes beyond import alignment

## Domain Model Impact

No domain invariants change.

Rule-schema policy and rule-document class semantics remain domain-owned and are consumed by the new service.

## Owning Layer

Application.

## Execution Plan

Execution Order:

1. create `services/rule_schema_validation/` with a minimal public shim
2. move `RuleSchemaValidationResult` into the folder
3. move `RuleSchemaDriftFinding` into the folder
4. move `RuleSchemaReportBuilder` into the folder
5. move validation orchestration into `RuleSchemaValidationService`
6. rewrite `DescribeRuleSchemaDrift` as thin delegation
7. align application and service exports with the new boundary
8. update tests that import the public validation result type

Allowed Adaptations:

1. keep the existing helper name `RuleSchemaReportBuilder` if it still adds clarity
2. additional internal helper files may be introduced only if they remain private to the folder
3. constructor dependency wiring may shift from the query into the service

Stop And Ask If:

1. the public feature boundary needs to expose additional internal rule-schema types beyond the current result type
2. the validation DTOs are discovered to belong outside application
3. the service extraction would require changing domain or infrastructure ownership

Implementation Notes:

1. use `RuleSchemaValidationService.describe(...) -> RuleSchemaValidationResult`
2. keep `RuleSchemaValidationResult` publicly importable from `application` after the move
3. keep folder-internal helper classes hidden behind `rule_schema_validation/__init__.py`

## Verification

1. `DescribeRuleSchemaDrift` contains one query class only
2. the query delegates to `RuleSchemaValidationService`
3. `RuleSchemaValidationResult` remains publicly importable from `application`
4. no code outside the folder imports deep internal validation helpers
5. rule-schema application and UI tests still pass after updates

## Completion Criteria

1. rule-schema validation is isolated behind one folder boundary
2. DTOs and helpers owned by that concern no longer sit as loose sibling files under `services/`
3. the query is thin and parameter-simple

## Handoff Notes

This step is the main compliance step for the local service-folder rule because it collapses a multi-file concern behind one explicit boundary.
