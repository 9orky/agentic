# Infrastructure Layer Rules

Read this file when the task affects persistence, subprocesses, filesystem, network, external services, or concrete adapter implementations.

## Ownership

`infrastructure` owns:

1. repository implementations
2. persistence mappings
3. external clients and runtime integrations
4. serialization and technical-boundary translation
5. concrete implementations of abstractions owned by `domain` or `application`

`infrastructure` may depend on `domain`, but not on `application` or `ui`.

## Layout Constraints

1. Use `repository` as the anchor when infrastructure implements repository contracts.
2. If repository implementation needs multiple files, use `repository/` rather than loose sibling files.
3. Larger integrations may split by external system or adapter type as long as ownership stays in infrastructure.
4. Cross-layer consumers may import infrastructure symbols only through `infrastructure/__init__.py` or the owning anchor shim.

## Placement Rules

1. Put concrete adapters here, not in `application`.
2. Keep external-system types and mappings here.
3. Do not move workflow or business rules into infrastructure to simplify wiring.

## Acceptance Check

1. Concrete adapters live in infrastructure, not in other layers.
2. Infrastructure depends only inward on domain.
3. Repository implementations stay behind the repository anchor when that anchor exists.
4. No cross-layer deep imports remain.