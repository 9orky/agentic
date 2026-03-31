# Goal

Split the current `workspace_contract/contract` module into smaller sibling modules so sync responsibilities and rule-schema audit responsibilities have separate ownership, while preserving the feature-root public seam in `workspace_contract/__init__.py` and `workspace_contract/cli.py`.

# Planned Blast Radius

Scope:
- Reshape the internal module anatomy of the `workspace_contract` feature.
- Preserve current user-facing behavior for `init`, `update`, `check-rules`, and the feature-root Python API.
- Keep the split close to a move-and-rewire refactor instead of a behavioral rewrite.

Owning Enclosure, Public Boundary, And Public Seam:
- Owning enclosure: `src/agentic/features/workspace_contract/`
- Public boundary: the `workspace_contract` feature root
- Public seam: `workspace_contract/__init__.py` for Python callers and `workspace_contract/cli.py` for CLI registration
- Internal target modules: `workspace_sync` and `rule_schema_audit`

Affected Features:
- `workspace_contract`
- No planned behavior or ownership changes for `architecture_check` or packaged rule resources

Layer Placement:
- `workspace_sync` owns sync-related domain policy usage, filesystem adapters for reading and writing workspace contract files, application commands and queries for bootstrap, update, and summary, and UI views for sync reporting.
- `rule_schema_audit` owns rule-schema validation policy usage, markdown parsing and rule-tree inspection adapters, the audit query path, and the UI view for schema findings.
- The feature root remains a thin composition and compatibility boundary only.

Dependency Direction:
- Feature root may depend on sibling module public seams.
- `ui` depends on `application` only through application-layer shims.
- `application` depends on the owning module's `domain` and `infrastructure` shims.
- `infrastructure` depends on its owning module's `domain` only where required by adapter contracts.
- Sibling modules must not deep-import each other's internals; any needed cross-module collaboration must go through an exported seam at the sibling module root.

Architectural Risk Check:
- SSOT: The main risk is duplicating sync or validation composition logic while splitting exports. The plan keeps one composition entrypoint per use case and one preserved feature-root seam.
- DRY: The main risk is cloning shared filesystem or reporting helpers into both modules. Shared responsibilities stay with the owning module unless a stable shared seam is demonstrated.
- YAGNI: The plan intentionally stops at two internal modules. It does not create extra reporting, summary, or shared-kernel modules up front.
- SOLID: The current `contract` module has multiple reasons to change. The split should improve single responsibility without introducing brittle circular seams between the new siblings.

Decision Log:
- Keep the feature-root API stable during the split.
- Start with two sibling modules, not three, because workspace summary still aligns with sync behavior more than with schema audit.
- Treat this as an internal module-boundary refactor, not a strategic domain rename or new bounded context.

# Strategic Model

Business Capability, Bounded Context, And Subdomain:
- Business capability: bootstrap and inspect the local agent collaboration contract for a project workspace
- Bounded context: `Workspace Contract`
- Subdomain: supporting tooling
- Colocated `DDD.md`: not planned for this split because business language, bounded-context identity, and external context relationships remain unchanged; this plan changes internal module ownership only

Extracted Domain Concepts:
- `Workspace Contract Sync`
  - classification: application coordinator built over an existing domain policy
  - identity: the sync use-case family that creates, updates, and summarizes managed workspace-contract assets
  - invariants: packaged shared rules remain the source of truth, local overrides remain preserved, and config/bootstrap files keep current overwrite rules
  - lifecycle: already exists and is being moved behind a narrower module seam
  - owning layer: `application`, backed by the existing sync policy in `domain`
- `Rule Schema Audit`
  - classification: application coordinator built over an existing domain policy
  - identity: the audit use-case family that parses rule documents and reports schema drift findings
  - invariants: packaged rule schema remains authoritative, local mirror validation stays optional, and findings preserve current codes and reporting shape
  - lifecycle: already exists and is being moved behind a narrower module seam
  - owning layer: `application`, backed by the existing schema policy in `domain`
- `SyncPolicy`
  - classification: domain service
  - identity: policy for determining workspace contract changes and summary state
  - invariants: planned changes must reflect layout rules and overwrite semantics
  - lifecycle: unchanged behavior; may move to the domain area owned by `workspace_sync`
  - owning layer: `domain`
- `RuleSchemaPolicy`
  - classification: domain service
  - identity: policy for validating document shells and section requirements
  - invariants: violations must stay deterministic for a given parsed document profile
  - lifecycle: unchanged behavior; may move to the domain area owned by `rule_schema_audit`
  - owning layer: `domain`
- `WorkspaceContractLayout`
  - classification: value object
  - identity: canonical path layout for local contract files
  - invariants: path derivation remains deterministic for a project root
  - lifecycle: unchanged and potentially shared through one module seam if both siblings still need it
  - owning layer: `domain`

# Execution Shape

Application Orchestration:
- Keep the current feature-root command and query entrypoints working while internal application commands and queries are re-homed behind `workspace_sync` and `rule_schema_audit`.
- Move composition helpers with their owning use-case families so factories no longer assemble unrelated services from one broad `contract.application` surface.
- End with a thin compatibility layer only if temporary re-exports are still needed during migration.

Infrastructure Responsibilities:
- Re-home workspace read and write adapters with `workspace_sync`.
- Re-home markdown parsing, packaged rule enumeration, and rule-tree readers with `rule_schema_audit`.
- Keep any truly shared adapter exported through one explicit seam instead of sibling deep imports.

UI Responsibilities:
- Keep the feature CLI at the feature root.
- Route `init` and `update` through the `workspace_sync` seam and `check-rules` through the `rule_schema_audit` seam.
- Keep sync-summary and rule-schema views with the owning sibling module.

Assumptions:
- Existing tests around feature-root exports, CLI behavior, and application delegation remain the primary regression net.
- This split should not change CLI names, return shapes, or finding codes.
- Temporary compatibility re-exports are acceptable during migration, but the final state should remove unnecessary broad internal anchors.

Major Phases Or Steps:
1. Establish the target sibling-module seams and define which current responsibilities belong to `workspace_sync` versus `rule_schema_audit`.
2. Move the sync family into `workspace_sync` and rewire feature-root exports and CLI usage without changing external behavior.
3. Move the schema-audit family into `rule_schema_audit` and rewire feature-root exports and CLI usage without changing external behavior.
4. Remove or reduce the old `contract` compatibility layer, align tests with the approved seams, and verify the final feature anatomy.

Phase Inputs And Outputs:
1. Input: current `contract` module anatomy and public feature seam. Output: approved sibling-module target shape and preserved external contracts.
2. Input: sync commands, summary query, sync service family, and related adapters and views. Output: working `workspace_sync` seam with stable feature-root behavior.
3. Input: rule-schema query, validation service family, and related adapters and views. Output: working `rule_schema_audit` seam with stable feature-root behavior.
4. Input: migrated sibling modules and temporary compatibility shims. Output: final feature layout, reduced internal broad seam, and passing verification.

# Acceptance

Acceptance Criteria:
- `workspace_contract` exposes the same feature-root Python and CLI seams after the split.
- Internal responsibilities are split into at least `workspace_sync` and `rule_schema_audit`, each with clear layer ownership.
- No sibling module relies on deep imports into another sibling's internals.
- Existing sync behavior, schema audit behavior, and result shapes remain unchanged.
- The obsolete broad `contract` module is either removed or reduced to a temporary, explicitly transitional compatibility surface.

# Open Questions

Known Risks Or Open Questions:
- Does `WorkspaceContractLayout` remain shared infrastructure-facing domain state, or should one sibling own it and expose it through a seam?
- Do the current tests that intentionally import `contract.*` paths need a temporary compatibility window, or should they be moved immediately to the new seams?
- Should `describe_workspace_contract` stay with `workspace_sync`, or does it deserve its own inspection-oriented module later if reporting concerns grow?