# Application Layer Rules

Document Class: leaf

## Purpose

`application` owns use cases, workflow orchestration, and feature-to-feature coordination.

## Applies When

Read this file when the task affects use cases, workflow orchestration, or feature-to-feature coordination.

## Ownership

`application` owns:

1. commands and write-side use cases
2. queries and read-side use cases
3. workflow coordination and transaction boundaries
4. application-owned abstractions for outward capabilities
5. feature-to-feature adaptation

`application` may depend on `domain` and `infrastructure`, but not on `ui`.

## Core Rules

### Required Anchors

Under the shared default, `application/` is organized only behind these anchors:

1. `commands`
2. `queries`
3. `services` when reusable orchestration is needed
4. `adapters` when feature-to-feature adaptation is needed

Do not leave loose application-owned files directly under `application/` outside those anchors.

### Layout Constraints

1. `commands` and `queries` are required anchors.
2. If multiple handlers are needed, use package form for that anchor.
3. Reusable orchestration grows behind `services.py` or `services/`.
4. Cross-feature adaptation grows behind `adapters/`.
5. Cross-layer consumers may import application symbols only through `application/__init__.py` or the owning anchor shim.

## Constraints

### Placement Rules

1. Keep business concepts in `domain`, not `application`.
2. Keep technical adapters in `infrastructure`, not `application`.
3. Keep user-facing parsing and rendering in `ui`, not `application`.

## Acceptance Check

1. Every touched application file belongs to one of the allowed anchors.
2. Commands and queries remain the primary use-case seams.
3. Cross-feature adaptation stays in `application`.
4. No loose root files appear under `application/`.