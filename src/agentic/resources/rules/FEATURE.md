# Feature Rules

Use this document to define and protect feature boundaries.

This file is part of the durable `agentic/` collaboration contract, so feature guidance here should capture reusable project understanding rather than one-session tactics.

Treat a feature as a set of modules behind one public boundary. Apply `MODULE.md` inside the feature. Use this file for feature-level ownership and dependency rules.

Use this document to make feature-boundary decisions predictable.

Use the standard development run from `AGENT.md`.

This document specializes feature ownership and boundary decisions inside that shared run.

This document is not complete by itself for internal module structure or refactor execution.

Also read:

- `MODULE.md` for internal module shape and public entry-point rules
- `TESTS.md` when verification or test coverage changes
- `REFACTORING.md` when the feature work is a migration or replacement
- `PLANNING.md` when the feature work is driven by an approved plan step

Do not treat a missing instruction here as permission to break a relevant module, refactor, or plan rule.

## Core Rules

1. Expose one primary public feature boundary.
2. Export only the intended feature boundary from the feature's public entry point.
3. Do not allow cross-feature deep imports.
4. Keep internal helper modules out of the public API.
5. Keep consumer-owned orchestration in the consumer.
6. Do not re-export a secondary boundary module through the feature's primary public entry point.

## Feature Execution Focus

During the shared run, focus on these feature-specific checkpoints:

1. confirm the owning feature
2. confirm the public feature seam
3. confirm which collaboration stays inside the consumer
4. isolate unfinished downstream dependencies locally if needed
5. verify through the feature boundary

## Feature As A Set Of Modules

Split feature responsibilities into internal modules as needed.

Typical internal modules include:

- ports
- adapters
- services
- policies
- models
- orchestration
- phases

Keep those modules internal unless there is a deliberate public reason to expose something through the feature boundary.

## Ownership

- the contract layer owns caller-facing data shapes
- the shared domain layer owns shared domain language
- each feature owns its local internals and models
- the shared/common layer owns generic helpers only

Keep one owner per concept. Do not create a fake universal type layer.

If the project has ownership exceptions, document them in `_PROJECT.md`.

## Boundary Rules

1. Communicate across features only through the target feature boundary or public entry point.
2. If another feature needs a capability, expose it through the public feature boundary instead of exporting helpers.
3. Do not export validators, adapters, registries, resolvers, stages, or similar internal mechanics.
4. Keep cross-feature adaptation in the consuming feature when practical.
5. If a downstream feature is unfinished, isolate it behind a local port and stub adapter.
6. If a feature owns more than one boundary module, import the needed seam from that boundary module directly.
7. Do not surface a feature's cli seam through `__init__.py` just to shorten imports.

If another feature needs a helper instead of a capability, do not export the helper. Either keep the adaptation in the consumer or promote a deliberate capability to the feature boundary.

## Dependency Rules

1. Keep the dependency graph acyclic.
2. Do not let lower-level features depend on their consumers.
3. Let consumers derive artifacts from other feature decisions only when ownership stays with the consumer.

If the project uses a specific layer map or allowed dependency direction, document it in `_PROJECT.md`.

## Ownership Defaults

When feature ownership is unclear, use these defaults:

1. the feature that owns the business invariant owns the decision logic
2. the consuming feature owns artifacts derived from another feature's output
3. boundary translation belongs at the consumer side unless the owning feature deliberately exposes a stable external contract
4. unfinished downstream collaboration should be hidden behind a local port, not solved with deeper imports

If two features could own something, prefer the owner with the narrower stable responsibility.

## Relation To Module Rules

Read `MODULE.md` for:

- file naming patterns
- one-primary-construct-per-file guidance
- public entry point rules for module APIs
- module-boundary rules inside a feature

Use this file for:

- the public feature boundary
- ownership across features
- dependency direction between features
- internal module composition inside one feature

## Acceptance Check

Before accepting a feature change, verify:

1. the owning feature is clear
2. the public boundary is still the intended feature seam
3. internal modules remain internal by default
4. the feature public entry point is minimal
5. other features do not reach behind the boundary
6. the implementation follows `MODULE.md`

## Fallback Guidance

When feature progress is blocked by an unfinished neighbor:

1. keep the public feature boundary clean
2. add a local port in the consumer
3. use a stub or adapter locally
4. avoid exporting new helper internals from the neighbor just to unblock work

This keeps work moving without normalizing hacks into the architecture.

If the fallback changes module shape inside the feature, re-check `MODULE.md` before implementing it.

Keep the run shape stable: inspect, define feature seam, implement minimal slice, verify through the boundary.