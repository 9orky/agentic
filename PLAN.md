# Workspace Contract Application Refactor Plan

## Goal
Refactor the `workspace_contract` application layer so it complies with this repository's local application rules.

Target outcome:
1. `commands/` and `queries/` remain required and keep one command or query per file
2. commands and queries stay as thin seams that accept only simple parameters and delegate orchestration
3. orchestration moves into application services
4. any service that needs more than one file moves into its own folder with a minimal public API

This plan stays at the high-level boundary and contract level. It defines the target application anatomy and intended class boundaries. It does not replace the executable step files.
Any step files derived from this plan must follow the active planning contract and use exactly one `Planned Blast Radius` section placed directly under `Goal`.

## Planned Blast Radius
Scope:

1. `src/agentic/features/workspace_contract/contract/application/`
2. application-facing imports re-exported by `workspace_contract`
3. test updates needed to preserve the public application seam while allowing internal service refactors

Out of Scope:
1. changing the `workspace_contract` feature boundary
2. moving domain or infrastructure responsibilities into different layers
3. changing CLI behavior beyond the minimum needed to keep imports aligned with the refactored application layer

Owning Enclosure, Public Boundary, And Public Seam:
The owning enclosure is `src/agentic/features/workspace_contract/contract/`.

The public boundary for this refactor is the `workspace_contract` feature seam used by:
1. `src/agentic/features/workspace_contract/__init__.py`
2. `src/agentic/features/workspace_contract/contract/ui/cli.py`
3. existing application-level imports consumed by tests
The public seam that must remain stable is:

1. `BootstrapProject`
2. `UpdateProject`
3. `DescribeWorkspaceContract`
4. `DescribeRuleSchemaDrift`
5. `RuleSchemaValidationResult`
Affected Features:

`workspace_contract` owns:
1. all command and query seams under `contract/application`
2. all application orchestration services needed by those seams
3. the application DTOs used to report rule-schema validation results

No other feature should own this refactor.
Layer Placement:

Application:
1. `WorkspaceContractSyncService`
2. `WorkspaceContractSummaryService`
3. `RuleSchemaValidationService`
4. `RuleSchemaValidationResult`
5. `RuleSchemaDriftFinding`
6. any internal result-builder or comparator class needed only to support one service folder

Domain:
1. `SyncPolicy`
2. `RuleSchemaPolicy`
3. `WorkspaceContractLayout`
4. `WorkspaceContractSummary`
5. rule-document classification values and invariants

Infrastructure:
1. `PackagedRulesReader`
2. `WorkspaceReader`
3. `WorkspaceWriter`
4. `RuleMarkdownParser`
5. `RuleTreeReader`
6. `RuleMarkdownDocument`

UI:
1. CLI command binding
2. sync summary rendering
3. rule-schema drift rendering

Dependency Direction:
Cross-layer direction:

1. `ui` depends on `application`
2. `application` depends on `domain` and `infrastructure`
3. `infrastructure` may depend on `domain`
4. `domain` depends on nothing above it

Within `application`:
1. `commands` depend on `services`
2. `queries` depend on `services`
3. `application/__init__.py` depends only on command, query, and minimal service exports
4. command and query files do not depend on each other

Architectural Risk Check:
1. SSOT: each application concern must end with one owning orchestration surface; command or query files must not retain duplicate orchestration paths after service extraction.
2. DRY: bootstrap and update must share one sync service instead of duplicating orchestration, and rule-schema validation must stop existing as several loose sibling files without a single owning boundary.
3. YAGNI: do not add new feature seams, boundary DTOs, or compatibility layers unless they are required to preserve the current public API.
4. SOLID: commands and queries remain thin, services own coordination, DTOs stay data-only, and domain and infrastructure responsibilities stay in their current layers.

Decision Log:
1. preserve existing public command, query, and result names unless a rename is required to satisfy the local rules
2. keep `WorkspaceContractSummaryService` in single-file form unless the implementation proves that it owns additional internals
3. move the sync concern and the rule-schema validation concern behind explicit service boundaries because both already span multiple files or multiple public seams

## Strategic Model
Business Capability, Bounded Context, And Subdomain:

The business capability is workspace-contract orchestration for bootstrapping, updating, describing, and validating the local `agentic` contract.

The bounded context is `workspace_contract`.
The subdomain is application-layer coordination: turning domain policies and infrastructure readers and writers into use-case execution with a strict command, query, and service structure.

Extracted Domain Concepts:
Workspace Contract Sync Service:

Classification: application coordinator.

Identity: one application service responsible for bootstrap and update orchestration.

Invariants:
1. command classes do not perform sync orchestration themselves
2. bootstrap and update remain two command seams, even if they share one orchestration service
3. update behavior is selected by simple input, not inheritance

Lifecycle:
1. constructed by the application layer with domain policy and infrastructure collaborators
2. invoked by `BootstrapProject` or `UpdateProject`
3. returns the same externally visible sync-result shape now expected by the feature boundary

Owning Layer: application.
Workspace Contract Summary Service:

Classification: application coordinator.

Identity: one application service responsible for workspace summary orchestration.

Invariants:
1. the query class remains a thin seam
2. summary assembly stays outside the query file
3. the returned summary remains the domain-owned `WorkspaceContractSummary`

Lifecycle:
1. constructed with the existing domain policy and workspace readers
2. invoked only by the summary query
3. returns the assembled domain summary

Owning Layer: application.
Rule Schema Validation Service:

Classification: application coordinator.

Identity: one application service responsible for rule-schema validation orchestration.

Invariants:
1. `DescribeRuleSchemaDrift` remains a thin query seam
2. validation orchestration, local-vs-packaged comparison, and finding aggregation live outside the query file
3. application-owned validation DTOs stay behind one service boundary

Lifecycle:
1. constructed with validation policy, parser, rule-tree readers, and workspace reader
2. invoked by the rule-schema query
3. returns the public validation result used by UI and feature exports

Owning Layer: application.
Rule Schema Validation Result:

Classification: application DTO.

Identity: one immutable result for a rule-schema validation run.

Invariants:
1. packaged documents, local documents, and findings remain grouped together
2. the DTO stays application-owned because it represents use-case output, not a domain invariant

Lifecycle:
1. created inside the rule-schema validation service boundary
2. returned through the query and rendered by the UI

Owning Layer: application.
Rule Schema Drift Finding:

Classification: application DTO.

Identity: one immutable finding inside a validation result.

Invariants:
1. each finding describes one scope, one document path, one violation code, and one message
2. findings remain internal to the rule-schema validation service boundary except for their inclusion in the public result

Lifecycle:
1. created during rule-schema validation
2. returned as part of the validation result

Owning Layer: application.
## Execution Shape

Application Orchestration:

The target application flow is:

1. `BootstrapProject` delegates directly to `WorkspaceContractSyncService.bootstrap(...)`
2. `UpdateProject` delegates directly to `WorkspaceContractSyncService.update(...)`
3. `DescribeWorkspaceContract` delegates directly to `WorkspaceContractSummaryService.describe(...)`
4. `DescribeRuleSchemaDrift` delegates directly to `RuleSchemaValidationService.describe(...)`
5. command and query files keep parameter intake, one service call, and return mapping only

Infrastructure Responsibilities:
This refactor continues using the current infrastructure collaborators without changing their ownership.

The main application-layer change is composition and delegation, not new infrastructure behavior.

UI Responsibilities:
The UI continues importing the same application seams.

The refactor should not require the CLI or views to understand the new internal service folder layout.

Assumptions:
1. the external feature API should stay stable during this refactor
2. keeping `RuleSchemaValidationResult` publicly importable from `application` is still required by current UI and tests
3. the sync use cases can share one orchestration service without weakening the command-level public seam
4. `DescribeWorkspaceContract` is simple enough to delegate to a single-file service unless new helper classes emerge
5. the rule-schema validation concern is complex enough to justify service-folder form with a minimal public API
6. existing helper and DTO names should be preserved unless a rename is required to satisfy the local rules

Major Phases Or Steps:
1. define the final target service boundaries and public exports for `application`
2. extract bootstrap and update orchestration into one sync-service boundary and remove command inheritance
3. extract workspace-summary orchestration into a dedicated summary service
4. move rule-schema validation orchestration, `RuleSchemaValidationResult`, `RuleSchemaDriftFinding`, and `RuleSchemaReportBuilder` behind one service folder with a minimal public API
5. align application exports, UI imports, and tests with the new internal layout
6. verify the final application tree satisfies the local application rules

Phase Inputs And Outputs:
Phase 1:

Input: current application files and local application rules.

Output: approved target application anatomy and public seam.

Phase 2:

Input: approved sync-service boundary.

Output: thin `BootstrapProject` and `UpdateProject` commands with composition instead of inheritance.

Phase 3:

Input: approved summary query implementation.

Output: thin `DescribeWorkspaceContract` query backed by `WorkspaceContractSummaryService`.

Phase 4:

Input: current rule-schema query and sibling DTO and service files.

Output: one `rule_schema_validation/` service boundary containing `service.py`, `rule_schema_validation_result.py`, `rule_schema_drift_finding.py`, and `rule_schema_report_builder.py`, plus thin query delegation.

Phase 5:

Input: refactored application internals.

Output: stable feature imports, aligned tests, and verified rule compliance.

## Acceptance

Acceptance Criteria:

1. `commands/` and `queries/` still exist and remain the only command and query anchors
2. each command file contains one command class only
3. each query file contains one query class only
4. command and query methods accept only simple parameters and do not contain orchestration logic
5. bootstrap and update no longer share logic through class inheritance
6. every multi-file service lives in its own folder with a minimal public API
7. `DescribeRuleSchemaDrift` no longer contains the current orchestration-heavy implementation body
8. the `workspace_contract` feature boundary keeps the same externally visible application seam unless an explicit follow-up plan approves a boundary change

## Open Questions

Known Risks Or Open Questions:

1. `SyncReportBuilder` may remain small enough for single-file form, but the sync concern already justifies a folder because the service boundary is shared by two commands
2. if `RuleSchemaValidationService` needs more internal helper classes than currently expected, the folder may need one additional internal helper file, but the service boundary should still export only the minimal API
3. tests currently import some application-level types directly; those imports need to remain stable or be changed deliberately in the same refactor
4. if the refactor reveals that `RuleSchemaValidationResult` is better treated as a feature-boundary DTO instead of an application export, that should be handled in a separate boundary-change plan rather than folded into this application-layout refactor
