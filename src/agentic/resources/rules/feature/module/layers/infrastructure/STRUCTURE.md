# Infrastructure Structure Rules

Document Class: leaf

## Purpose

Within the owning module's `infrastructure` layer, structure rules place repositories, concrete adapters, mappings, and translation logic behind named anchors.

## Applies When

Read this file when the task decides where a concrete adapter, repository implementation, mapper, serializer, or integration concern belongs inside `infrastructure`.

## Ownership

`infrastructure` structure owns:

1. repository implementations for domain-owned repository contracts
2. one named adapter anchor per external boundary, storage mode, runtime capability, or translation concern
3. boundary representations, persistence mappings, and serialization logic
4. concrete implementations selected by application-owned orchestration

`infrastructure` may depend on `domain`, but not on `application` or `ui`.

## Core Rules

### Anchor Contract

Under the shared default, `infrastructure/` is anchor-based.

Use these root forms:

1. `repository` when infrastructure implements domain-owned repository contracts
2. one named adapter anchor per external boundary, storage mode, runtime capability, or translation concern
3. one standalone adapter file at the layer root only when it owns a single concrete concern and does not need private substructure yet

Do not create generic buckets such as `helpers`, `utils`, `common`, or `misc` under `infrastructure`.

### Layout Constraints

1. Use `repository` as the anchor when infrastructure implements repository contracts.
2. If repository implementation needs multiple files, use `repository/` rather than loose sibling files.
3. If a standalone adapter grows private helpers or multiple concrete implementations, convert it to a same-named package.
4. Keep boundary translation and representation mapping behind the owning adapter anchor rather than as loose cross-cutting files.
5. Keep concrete concerns grouped by boundary ownership rather than by generic technical mechanism.

## Constraints

1. Put concrete adapters here, not in `application`.
2. Keep boundary representations and mappings here.
3. Do not move workflow or business rules into infrastructure to simplify wiring.
4. Do not import application internals from infrastructure; if an application-facing seam is needed, expose it from `application` and let application choose the adapter through its own boundary.

## Acceptance Check

1. Concrete adapters live in infrastructure, not in other layers.
2. Infrastructure depends only inward on domain.
3. Repository implementations stay behind the repository anchor when that anchor exists.
4. Root-level infrastructure files each own one concrete concern; larger concerns move behind a named anchor.
5. No cross-layer deep imports remain.