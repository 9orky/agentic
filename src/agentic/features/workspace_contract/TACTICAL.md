# Workspace Contract Tactical Plan

## Purpose

This document defines the tactical model for the `Workspace Contract` bounded context.

It explains how the `workspace_contract` feature, which is the current implementation root for that bounded context, expresses identity, invariants, ownership, and code-facing concepts.

## Scope

This tactical plan governs `src/agentic/features/workspace_contract/`.

It covers the current `contract` module and the bounded-context seams exposed through the feature root.

It should stay aligned with the repo-level strategic model in [DDD.md](../../../DDD.md).

## Model Decisions

1. The `workspace_contract` feature root is the current implementation root for the `Workspace Contract` bounded context, so this tactical artifact uses the strategic bounded-context name as its source of truth.
2. `project_root` is a stable external identifier for a managed workspace contract, but identity continuity is not yet rich enough to justify a dedicated entity or aggregate root.
3. Domain logic is centered on value objects plus policy-oriented domain services.
4. Application commands and queries are intentionally thin seams that delegate to service-owned orchestration instead of constructing lower-layer collaboration directly.
5. UI owns the CLI entrypoint, rendered summary and drift views, and path-presentation helpers while depending only on application seams.
6. No domain-owned repository contract exists yet because the bounded context reads and writes directly through infrastructure adapters without protecting a richer domain aggregate.

## Concept Catalog

| Concept | Classification | Identity | Invariants | Lifecycle | Owning Module | Owning Layer |
| --- | --- | --- | --- | --- | --- | --- |
| Workspace contract summary | Value object | Identified by the summarized `project_root` plus the captured contract state | Present and missing shared-rule paths stay normalized and sorted | Built on demand for describe operations and discarded after use | `contract` | `domain` |
| Workspace contract layout | Value object | Identified by deterministic path rules for the bounded context | Managed directories and file locations are derived consistently from the same layout rules | Constructed as needed by policies and infrastructure adapters | `contract` | `domain` |
| Shared rule path | Value object | Identified by a rules-tree-relative path | Must stay relative, non-empty, and inside the managed shared-rules tree | Created when enumerating or addressing packaged shared rules | `contract` | `domain` |
| Sync change | Value object | Identified by one shared rule plus one sync action | Destination path is derived from the active layout and shared rule path | Created during sync planning and consumed during execution | `contract` | `domain` |
| Rule document schema | Value object | Identified by document class and declared section requirements | A schema must define at least one section requirement | Built from the shared leaf or navigational schema factory | `contract` | `domain` |
| Rule section requirement | Value object | Identified by its allowed heading set | At least one non-empty heading must exist and the first heading is canonical | Created as part of a schema definition and reused for validation | `contract` | `domain` |
| Rule schema violation | Value object | Identified by code, message, and optional section heading | Violation records must remain immutable findings | Created during document validation and then returned to callers | `contract` | `domain` |
| Rule document class | Value object | Identified by the declared rule-document kind | The class must stay one of the supported schema kinds | Parsed from markdown and consumed during validation | `contract` | `domain` |
| Sync policy | Domain service and policy | One policy object for sync planning behavior | Shared-rule paths are sorted deterministically and sync actions are derived from current state plus overwrite intent | Constructed on demand and reused by sync-oriented application services | `contract` | `domain` |
| Rule schema policy | Domain service and policy | One policy object for rule-schema validation behavior | Required sections, ordering rules, and navigation-target rules are enforced consistently by document class | Constructed on demand and reused by validation-oriented application services | `contract` | `domain` |
| Workspace contract sync service | Application coordinator | One orchestration service for bootstrap and update use cases | Bootstrap preserves existing local state by default and update refreshes managed shared docs while preserving local extensions | Constructed by command seams, invoked per use case, then discarded | `contract` | `application` |
| Workspace contract summary service | Application coordinator | One orchestration service for describe use cases | Summary creation must be derived from the current packaged rules and observed workspace state | Constructed by query seams, invoked for summary generation, then discarded | `contract` | `application` |
| Rule schema validation service | Application coordinator | One orchestration service for rule-schema drift checks | Packaged and local documents are parsed and compared under the same policy and report format | Constructed by query seams, invoked for validation, then discarded | `contract` | `application` |
| Rule schema validation result | Application DTO | Identified by one rule-schema validation run | Packaged documents, local documents, and findings must remain grouped as one immutable validation result | Created during validation and then rendered or returned | `contract` | `application` |
| Rule schema drift finding | Application DTO | Identified by scope, document path, code, and document class for one finding | Each finding must remain an immutable report item tied to one validation result | Created during validation and then aggregated into a validation result | `contract` | `application` |
| Packaged rules reader | Infrastructure adapter | One adapter for packaged shared-rule resources | Only packaged source-of-truth documents are enumerated and loaded | Instantiated by application services when packaged resources are needed | `contract` | `infrastructure` |
| Workspace reader | Infrastructure adapter | One adapter for observed workspace state | Reads must respect the managed layout and ignore unmanaged directories where required | Instantiated by application services when filesystem state is needed | `contract` | `infrastructure` |
| Workspace writer | Infrastructure adapter | One adapter for managed workspace writes | Managed directories are created safely and writes create parent directories deterministically | Instantiated by application services when managed files must be written | `contract` | `infrastructure` |
| Rule markdown parser | Infrastructure adapter | One adapter for parsing rule markdown into structured documents | Parsed headings, anchors, and navigation targets must be derived consistently from source text | Instantiated by validation services when rule documents are parsed | `contract` | `infrastructure` |
| Rule tree reader | Infrastructure adapter | One adapter for enumerating packaged and local rule documents | Packaged and local document trees are enumerated deterministically | Instantiated by validation services when rule trees are compared | `contract` | `infrastructure` |
| Workspace contract CLI | UI contract | One registered delivery surface for `init`, `update`, and `check-rules` | Delivery depends only on application seams and preserves command names plus exit-code behavior | Registered at feature startup and invoked per CLI call | `contract` | `ui` |
| Sync summary and rule schema drift views | UI contract | Identified by one rendered response shape per operation | Rendering must remain delivery-only and format application results without owning domain or infrastructure rules | Instantiated per UI flow and discarded after rendering | `contract` | `ui` |
| Project path presenter | UI service | One path-formatting helper for UI rendering | Presented paths must be relative to the active project root when possible | Constructed on demand and reused within one rendering flow | `contract` | `ui` |

## Aggregate And Repository Decisions

1. No dedicated entity is modeled in the domain today.
2. No aggregate boundary is modeled today because the bounded context derives plans and summaries from current filesystem state instead of protecting a mutable consistency boundary.
3. No domain-owned repository contract exists today because there is no aggregate whose invariants require a domain-facing persistence abstraction.
4. If the bounded context later promotes `Workspace Contract` or `Managed Workspace Contract` into a true entity with lifecycle transitions, revisit aggregate and repository decisions first rather than adding an entity ad hoc.

## Open Questions

1. Should `Workspace Contract` become an explicit entity once lifecycle and state transitions matter beyond one operation?
2. Should drift findings remain application DTOs, or is there a future case for promoting part of that language into the domain model?
3. Is there a future aggregate boundary around managed shared-rule synchronization, or is the current value-object and policy model sufficient?