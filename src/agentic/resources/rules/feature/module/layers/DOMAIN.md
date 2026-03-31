# Domain Layer Rules

Document Class: leaf

## Purpose

Within the owning module, `domain` owns business concepts, invariants, and domain-owned abstractions.

## Applies When

Read this file when the task affects business concepts, invariants, or domain-owned abstractions inside the current module.

## Ownership

`domain` owns:

1. entities
2. value objects
3. domain services
4. policies and invariants
5. domain-owned repository contracts when they belong to the business language

`domain` must not depend on `application`, `infrastructure`, or `ui`.

## Core Rules

### Required Anchors

Under the shared default, `domain/` is organized only behind tactical anchors:

1. `entity` when the module owns entities or aggregate roots
2. `value_object` when the module owns value objects
3. `service` when the module owns domain services or policies that need their own classes
4. `repository` only when a real domain-owned repository contract exists

Do not place loose domain classes directly under `domain/` outside those anchors.

### Layout Constraints

1. Domain code is class-based under the shared default.
2. Free functions are forbidden in domain.
3. One class per file is mandatory in domain.
4. If an anchor needs more than one class, switch that anchor to package form.
5. Each anchor may be a file or a same-named package.
6. If a tactical concept such as entity, aggregate boundary, or repository is absent, keep that absence intentional and documented in planning guidance rather than adding a placeholder.
7. Cross-layer consumers may import domain symbols only through `domain/__init__.py` or the owning anchor shim.

## Constraints

### Placement Rules

1. Put repository contracts in `domain` only when they express domain language or protect domain invariants.
2. If an abstraction exists only as an execution dependency of a use case, it belongs in `application`, not `domain`.
3. Helper logic that cannot justify a domain class does not belong in `domain`.
4. Do not introduce generic buckets such as `helpers`, `utils`, or `common` under `domain`.
5. Every touched domain concept must have an explicit tactical classification even when no new code anchor is introduced.

## Acceptance Check

1. Every touched domain concept maps to an explicit tactical classification and, when implemented in code, to one anchor.
2. Domain stays free of outward dependencies.
3. The one-class-per-file rule remains intact.
4. No loose root classes or generic helper buckets appear under `domain/`.
5. Repository ownership is explicit rather than implied.