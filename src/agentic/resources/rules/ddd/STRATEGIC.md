# Strategic DDD Rules

Document Class: leaf

## Purpose

Use this file to define the strategic domain model for material domain work.

## Applies When

Use this file when the task changes business language, subdomains, bounded contexts, context relationships, or the strategic boundaries that planning must respect.

## Scope

1. Strategic DDD lives in a project-local `DDD.md` file.
2. Place `DDD.md` at the same directory level as the owning `PLAN.md`.
3. Keep ubiquitous language, subdomains, bounded contexts, context map, and boundary rules in `DDD.md` rather than scattering them across plans or step files.
4. Keep execution sequencing and implementation detail in `PLAN.md` and `PLAN_STEP_0X.md`, not in `DDD.md`.
5. When a bounded context has a stable implementation root, the strategic model should name that implementation root and its owning tactical-plan artifact.

## Core Rules

### Strategic Artifact Contract

1. Create or update `DDD.md` before approving a high-level plan when the work materially changes business language or domain boundaries.
2. Treat `DDD.md` as the durable strategic source of truth for domain terminology and boundaries.
3. Reuse the exact ubiquitous-language terms from `DDD.md` in plans, steps, code, and tests.

### Required Sections

`DDD.md` must include these sections:

1. `Purpose`
2. `Scope`
3. `Ubiquitous Language`
4. `Subdomains`
5. `Bounded Contexts`
6. `Context Map`
7. `Boundary Rules`
8. `Open Questions`

## Constraints

### Modeling Discipline

1. Distinguish business capabilities, subdomains, bounded contexts, and code structure explicitly instead of collapsing them into one list.
2. Name relationships between bounded contexts explicitly, including translation or conformity expectations when terms differ.
3. State whether each bounded context has its own `TACTICAL.md` artifact or an intentional shared or deferred tactical plan, and name the implementation root when one exists.
4. If the work is domain-adjacent but leaves the strategic model unchanged, record that decision explicitly instead of silently skipping strategic review.
5. Do not duplicate step sequencing, file trees, or implementation notes in `DDD.md`.

## Acceptance Check

1. Material domain work has a project-local `DDD.md` artifact or an explicit rationale for why the strategic model is unchanged.
2. Ubiquitous language, subdomains, bounded contexts, and context map are explicit.
3. Bounded contexts with a stable implementation root name that root plus their tactical-plan artifact, or explain the absence of either.
4. Plan terminology aligns with `DDD.md`.
5. `DDD.md` stays strategic rather than drifting into execution detail.