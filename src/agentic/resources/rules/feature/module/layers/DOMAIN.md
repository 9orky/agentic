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

### Core Constraints

1. Domain code is class-based under the shared default.
2. Free functions are forbidden in domain.
3. One class per file is mandatory in domain.
4. If an anchor needs more than one class, switch that anchor to package form.
5. Do not place loose domain classes directly under `domain/` outside a required anchor.

### Required Anchors

Use these anchors as the baseline shape:

1. `entity`
2. `value_object`
3. `service`
4. `repository` only when a real domain-owned repository contract exists

Each anchor may be a file or a same-named package.

## Constraints

### Placement Rules

1. Put repository contracts in `domain` only when they express domain language or protect domain invariants.
2. If an abstraction exists only as an execution dependency of a use case, it belongs in `application`, not `domain`.
3. Helper logic that cannot justify a domain class does not belong in `domain`.

### Layer Shim Rule

Other layers may consume domain symbols only through `domain/__init__.py` or the owning anchor shim.

## Acceptance Check

1. Every touched domain concept maps to one anchor.
2. Domain stays free of outward dependencies.
3. The one-class-per-file rule remains intact.
4. Repository ownership is explicit rather than implied.