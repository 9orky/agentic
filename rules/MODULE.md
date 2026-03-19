# Module Rules

Use this document to shape directories and files as modules.

Treat a module as a directory, package, or equivalent boundary by default. Treat a feature as a set of modules. Use `FEATURE.md` for feature-level rules and this file for module-level structure.

Use this document to make module decisions predictable.

Use the standard development run from `AGENT.md`.

This document specializes module decisions inside that shared run.

This document is not complete by itself when the module belongs to a feature or is being refactored.

Also read:

- `FEATURE.md` when the module change affects a feature boundary or cross-feature collaboration
- `TESTS.md` when verification or test coverage changes
- `REFACTORING.md` when the module change is part of migration, replacement, or structural cleanup
- `PLANNING.md` when the module change is governed by an approved plan step

Do not treat a missing instruction here as permission to break a relevant feature, refactor, or plan rule.

## Core Rules

1. Treat every directory, package, or equivalent container as a module boundary.
2. Keep the public API minimal.
3. Publish the module API through the module's public entry point.
4. Do not import from behind another module's public entry point.
5. Keep helpers, policies, services, and models inside the owning module.

## Module Execution Focus

During the shared run, focus on these module-specific checkpoints:

1. confirm the owning module boundary
2. confirm the intended public API in the module's public entry point
3. confirm which symbols stay internal
4. make the smallest structural change that satisfies the task
5. verify that no caller needs a deep import after the change

## Ownership Defaults

When ownership is unclear, use these defaults:

1. the module that defines the policy owns the policy logic
2. the module that defines the public contract owns the boundary mapping for that contract
3. the consumer owns derived artifacts created from another module's output
4. shared/common code belongs in a shared location only if it is truly generic and not feature-specific

If ownership is still ambiguous, prefer the narrower local owner over a broader shared location.

## File Naming Patterns

Use descriptive file and directory names that match the project's naming convention.

Use these role-based naming patterns by default when the stack supports them:

- the project's standard public entry file for the module public API
- `something-feature` for a feature boundary
- `something-service` for an internal service
- `something-adapter` for an adapter
- `something-validator` for validation logic
- `something-policy` for policy logic
- `something-types` only when a dedicated type or interface file is justified

Choose names that describe responsibility. Do not use vague technical filler names.

## One Primary Construct Per File

Keep one primary construct per file by default.

Break this rule only for a tiny helper that has no independent value outside the file.

Do not create extra files only to satisfy the rule mechanically. Cohesion is more important than ceremony.

## Public API Rule

Expose the smallest possible public surface through the module's public entry point.

That means:

- export only what other modules may depend on
- do not export helpers for convenience
- do not export intermediate models unless they are deliberate public contract
- keep construction details internal when the module can own them

If unsure whether something should be public, keep it internal first.

Do not widen the public API for local convenience.

## Caller And Orchestration Rule

Keep caller-owned orchestration in the shared parent or root module.

Do not force a child module to expose multiple internals so a parent can assemble them manually.

Prefer one child-owned entry seam.

If the child cannot yet own a clean seam, keep orchestration in the caller temporarily and keep the child internals private.

## Dependency Rule

Keep module dependencies directional and readable.

Do not introduce:

- deep imports into another module
- circular dependencies
- shared dumping-ground modules for feature-specific code
- leaked child-module assembly details in parent modules

## Acceptance Check

Before accepting a module shape, verify:

1. the module boundary has a clear ownership boundary
2. the public entry point is minimal
3. every public export is intentional
4. primary constructs live in their own files by default
5. other modules do not reach behind the public entry point

## Fallback Guidance

When a module rule and local delivery pressure conflict:

1. preserve the module boundary
2. avoid deep imports
3. choose the smallest internal change that works
4. do not add fake public seams just to unblock a caller

If progress still requires a public contract change, stop and ask.

If the module change also affects feature ownership or refactor sequencing, resolve that through `FEATURE.md` or `REFACTORING.md` before proceeding.

Keep the run shape stable: inspect, define module seam, implement minimal slice, verify the public entry point and boundaries.
