# High-Level Planning Rules

Document Class: leaf

## Purpose

Use this file to define the high-level plan before any executable step files exist.

## Applies When

The first planning response is the big-picture plan. Do not create step files until that plan is accepted.

## Scope

Keep the high-level plan at the boundary and contract level before file-level execution planning begins.
If the work materially changes business language, bounded contexts, context relationships, or domain structure, create or update a project-local `DDD.md` at the same directory level as the owning `PLAN.md`.

## Core Rules

### Required Content

Keep the high-level plan at the boundary and contract level.

Each high-level plan must include these sections:

1. `Goal`
2. `Planned Blast Radius`
3. `Strategic Model`
4. `Execution Shape`
5. `Acceptance`
6. `Open Questions`

When material domain work is in scope, the plan must also name the colocated `DDD.md` artifact that holds the strategic domain model.

`Planned Blast Radius` must be the second section, directly under `Goal`.

`Planned Blast Radius` must use labeled blocks instead of additional section headers for these items:

1. `Scope`
2. `Owning Enclosure, Public Boundary, And Public Seam`
3. `Affected Features`
4. `Layer Placement`
5. `Dependency Direction`
6. `Architectural Risk Check`
7. `Decision Log`

`Architectural Risk Check` must contain concrete bullets for:

1. `SSOT`
2. `DRY`
3. `YAGNI`
4. `SOLID`

Each bullet must state the expected risk, constraint, or explicit non-goal for that principle in the current plan.

`Strategic Model` must use labeled blocks instead of additional section headers for these items:

1. `Business Capability, Bounded Context, And Subdomain`
2. `Extracted Domain Concepts`

For each material concept, state:

1. classification
2. identity
3. invariants
4. lifecycle
5. owning layer

`Execution Shape` must use labeled blocks instead of additional section headers for these items:

1. `Application Orchestration`
2. `Infrastructure Responsibilities`
3. `UI Responsibilities`
4. `Assumptions`
5. `Major Phases Or Steps`
6. `Phase Inputs And Outputs`

`Acceptance` must contain `Acceptance Criteria`.

`Open Questions` must contain `Known Risks Or Open Questions`.

### Strategic Domain Modeling

Before locking the plan:

1. decide whether the work requires a colocated `DDD.md` artifact and create or update it when the strategic model changes materially
2. name the bounded context or business slice being changed
3. extract the candidate concepts implied by the request and current behavior
4. classify each concept as an entity, value object, domain service, repository, policy, event, application coordinator, infrastructure adapter, or UI contract
5. state the identity, invariants, lifecycle, and owning layer for each material concept
6. stop and tighten the model if a concept cannot be classified or placed deterministically

## Constraints

### Placement Rule

Do not leave placement implicit. If a touched responsibility cannot be placed clearly in the governing feature anatomy, the plan is not ready.

### Review Rule

The blast-radius section must let a human architect inspect structural risk before reading the rest of the plan.

### Handoff To Step Planning

After the high-level plan is accepted:

1. split the approved plan into executable step files named `PLAN_STEP_0X.md`
2. place every `PLAN_STEP_0X.md` file at the same directory level as the owning `PLAN.md`
3. do not create nested planning subdirectories for step files
4. keep the colocated `DDD.md` aligned with the approved strategic model before step files are written
5. keep the step sequence aligned with the approved phase order
6. move file-level implementation detail, target file naming, and step verification into the step files rather than overloading the big-picture plan

## Acceptance Check

1. The high-level plan stays at the boundary and contract level.
2. The plan contains the required sections, with `Planned Blast Radius` second.
3. Material domain work names a colocated `DDD.md` artifact or explicitly states why the strategic model is unchanged.
4. Material concepts are classified and placed deterministically.
5. The blast-radius section lets a human reviewer inspect SSOT, DRY, YAGNI, and SOLID risk before reading the rest of the plan.
6. Step files are not created before the high-level plan is accepted.
7. The plan names phases, acceptance criteria, and open questions explicitly.