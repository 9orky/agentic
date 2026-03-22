# Infrastructure Layer Rules

Document Class: leaf

## Purpose

Within the owning module, `infrastructure` owns persistence, integrations, serialization, and concrete adapters.

## Applies When

Read this file when the task affects persistence, storage adapters, boundary translation, execution-environment integrations, external capability adapters, or concrete adapter implementations inside the current module.

## Ownership

`infrastructure` owns:

1. repository implementations
2. persistence mappings
3. external capability adapters and execution-environment integrations
4. representation mapping and boundary translation
5. concrete implementations of abstractions owned by `domain` or `application`

`infrastructure` may depend on `domain`, but not on `application` or `ui`.

## Core Rules

### Layout Constraints

1. Use `repository` as the anchor when infrastructure implements repository contracts.
2. If repository implementation needs multiple files, use `repository/` rather than loose sibling files.
3. Larger integrations may split by external system or adapter type as long as ownership stays in infrastructure.
4. Cross-layer consumers may import infrastructure symbols only through `infrastructure/__init__.py` or the owning anchor shim.

## Constraints

### Placement Rules

1. Put concrete adapters here, not in `application`.
2. Keep boundary representations and mappings here.
3. Do not move workflow or business rules into infrastructure to simplify wiring.

## Acceptance Check

1. Concrete adapters live in infrastructure, not in other layers.
2. Infrastructure depends only inward on domain.
3. Repository implementations stay behind the repository anchor when that anchor exists.
4. No cross-layer deep imports remain.