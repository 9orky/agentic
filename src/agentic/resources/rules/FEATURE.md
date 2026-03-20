# Feature Rules

A feature owns one business capability and one public boundary.

This document defines the shared default feature anatomy. It is a constraint, not a preference.

The public boundary is the externally visible contract of the feature. The public seam is the single entry point to that boundary.

A feature enclosure may grow internally, but it must not spread responsibilities, seams, or coordination outside its boundary.

## Active Anatomy

1. This file defines the default feature anatomy shipped by the package.
2. A project may replace it through `rules/overrides/FEATURE.md` and any companion files it names.
3. If a repo-local override defines a different anatomy, that local anatomy governs.
4. Different local anatomy is not a defect by itself. The requirement is determinism, not sameness across repositories.
5. A repo-local anatomy must be documented with the same precision as this default: clear structural parts, ownership, dependency direction, public seams, and acceptance checks.
6. If the code clearly follows a different stable anatomy but the local docs do not define it, stop before structural refactoring and document or confirm that anatomy first.

## Default Shape

1. Keep each feature in its own folder.
2. Give the feature one public boundary reached through one public seam.
3. Under the shared default, use exactly these top-level layers: `ui/`, `application/`, `infrastructure/`, and `domain/`.
4. Under the shared default, do not add sibling root buckets such as `contracts/`, `ports/`, `adapters/`, `services/`, `types/`, or `utils/`.
5. Internal file names and subfolders may vary, but every file must belong clearly to one owning part of the governing anatomy.
6. Keep feature-to-feature adaptation inside the owning coordination part. Under the shared default, that part is `application`.

## Default Dependency Direction

Under the shared default:

1. `ui` may depend only on `application`.
2. `application` may depend on `domain` and `infrastructure`.
3. `infrastructure` may depend on `domain`.
4. `domain` must not depend outward.

Forbidden examples:

1. `ui -> domain`
2. `ui -> infrastructure`
3. `application -> ui`
4. `infrastructure -> application`
5. `domain -> application`
6. `domain -> infrastructure`

## Default Ownership

### `domain/`

- business rules and core domain concepts
- entities, value objects, policies, invariants, and pure transforms
- business-owned abstractions
- no outward dependencies

### `infrastructure/`

- external systems, runtime integrations, persistence, filesystem, network, subprocess, framework, and serialization details
- implementations of abstractions owned by `domain` or `application`
- technical-boundary translation
- may depend on `domain`, but not on `application` or `ui`

### `application/`

- use cases, orchestration, workflow coordination, and feature-to-feature adaptation
- translation needed to execute a use case
- application-owned abstractions for outward capabilities
- may depend on `domain` and `infrastructure`, but not on `ui`

### `ui/`

- the outermost delivery layer
- command handlers, controllers, route handlers, presenters, renderers, and request or response mapping
- input collection, output formatting, and user-facing interaction concerns
- thin coordination only; business rules and workflow logic do not live here
- may depend only on `application`

## Default Placement Rules

Under the shared default:

1. Do not create a root-level `contracts` bucket. Put types where their meaning belongs.
2. Do not create a root-level `ports` bucket. Put abstractions where their reason belongs.
3. Business abstractions belong in `domain`.
4. Outward capability abstractions used by use cases belong in `application`.
5. External-system types belong in `infrastructure`.
6. Input and output types belong in `ui`.

A repo-local replacement must define equally clear placement rules for its own parts.

## Cross-Feature Rules

1. External callers use the feature boundary through its public seam only.
2. Cross-feature calls go through the target feature boundary, never internal files.
3. Cross-feature adaptation stays in the owning coordination part. Under the shared default, that part is `application`.
4. Under the shared default, `domain` must not depend on another feature, including another feature's public types or errors.
5. Do not export helpers, mappers, validators, or intermediate models from the feature boundary.
6. Do not let cross-feature pressure collapse the enclosure or move foreign logic into the wrong owner.

## Acceptance Check

1. The feature boundary and public seam are clear and minimal.
2. When the shared default governs, the feature root contains only the four layer folders and the minimum public seam files.
3. Every internal file belongs clearly to one owning part of the governing anatomy.
4. Dependency direction matches the governing anatomy.
5. Cross-feature work stays in the owning coordination part defined by the governing anatomy.
6. Callers do not deep-import feature internals.
7. The implemented shape follows the governing feature rules as a constraint.
8. The enclosure allows internal growth without spreading ownership, seams, or coordination outside it.
9. The enclosure produces deterministic ownership, routing, and change placement.