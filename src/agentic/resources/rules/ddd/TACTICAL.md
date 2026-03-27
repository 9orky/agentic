# Tactical DDD Rules

Document Class: leaf

## Purpose

Use this file to define tactical domain-modeling decisions for the current bounded context.

## Applies When

Use this file when the task needs explicit tactical classifications, aggregate boundaries, repository ownership, or code-facing domain ownership decisions.

## Scope

1. Tactical DDD covers concept classification, identity, invariants, lifecycle, aggregate boundaries, and repository ownership inside the current bounded context.
2. Each bounded context with a stable implementation root should keep its own `TACTICAL.md` artifact near that root, even when the directory is named after a feature or package nickname.
3. Use this file together with the project-local `DDD.md` artifact and the owning feature and module rules.

## Core Rules

### Tactical Artifact Contract

1. Keep one tactical-plan artifact per bounded context unless several implementation roots intentionally share one model.
2. Name the bounded context explicitly in its `TACTICAL.md` artifact, using the same term as the strategic model rather than only a feature or package nickname.
3. If the tactical artifact lives under a differently named feature or package path, state that the path is the implementation root for the bounded context.
4. Keep the tactical plan code-facing: concept classification, ownership, aggregate boundaries, and repository decisions belong here.
5. Keep strategic language, subdomain boundaries, and context-map decisions in `DDD.md` rather than duplicating them here.

### Required Sections

Each bounded-context `TACTICAL.md` artifact must include:

1. `Purpose`
2. `Scope`
3. `Model Decisions`
4. `Concept Catalog`
5. `Aggregate And Repository Decisions`
6. `Open Questions`

### Required Classifications

1. Classify each material concept as one of these when applicable: entity, value object, aggregate, repository, domain service, factory, policy, or domain event.
2. For each material concept, state identity, invariants, lifecycle, owning module, and owning layer.
3. If a concept cannot be classified deterministically, tighten the model before coding.

### Tactical Minimums

1. Do not force every tactical pattern into every module.
2. Missing tactical elements such as entity, aggregate, repository, or domain event must be intentional and explained.
3. Introduce a repository only when a domain-facing abstraction protects domain language or invariants.
4. Introduce an aggregate only when a real consistency boundary must be defended.
5. Prefer value objects, policies, and services when identity continuity is not part of the model.

## Constraints

### Code Placement

1. Tactical DDD informs code placement but does not override feature and layer ownership rules.
2. Keep one authoritative name per concept across `DDD.md`, plans, code, and tests.
3. Revisit the strategic model if tactical decisions reveal a hidden context split or translation boundary.

## If Ambiguous, Go To

### Placement And Ownership

When tactical classification is clear but module or layer placement is still unresolved, route to [../feature/FEATURE.md](../feature/FEATURE.md) and then to the owning module-layer rule.

## Acceptance Check

1. The bounded context has its own `TACTICAL.md` artifact or an explicit rationale for sharing or deferring one.
2. Every material concept is classified or explicitly deferred.
3. Identity, invariants, lifecycle, and ownership are stated for each material concept.
4. Missing entity, aggregate, repository, or domain-event patterns are intentional rather than accidental.
5. Plans and code keep the same concept names as `DDD.md`, and the tactical artifact clearly maps its implementation root back to that bounded context.