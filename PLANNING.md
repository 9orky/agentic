# Planning

Use this document to create, approve, and expand plans.

Use the standard development run from `AGENT.md`.

This document specializes the planning part of that run. It does not replace the shared run shape.

This document is not sufficient by itself for architecture or boundary decisions.

If a plan touches module structure, feature boundaries, or refactor strategy, also read the matching scoped document before executing:

- `MODULE.md` for module structure
- `FEATURE.md` for feature ownership and boundaries
- `TESTS.md` for verification strategy when the plan defines tests
- `REFACTORING.md` for migration and replacement work

Do not treat missing architecture detail here as permission to improvise against those documents.

Planning always has two phases:

1. produce one high-level plan for approval
2. only after that plan is accepted, split it into `PLAN_STEP_X.md` files

Do not create, keep, or treat `PLAN_STEP_X.md` files as active execution plans before the high-level plan is accepted.

Treat the approved high-level plan as the contract. A step plan may change internally, but it must not silently change approved inputs, outputs, or acceptance intent.

## Planning Goal

Make the next correct action obvious.

Make repeated agent runs similar by making the execution order, boundaries, and verification path explicit before coding starts.

The plan should remove uncertainty about:

- what is being changed
- what must stay stable
- what success looks like
- when the agent may adapt internally without asking
- when the agent must stop and ask

## Planning Flow

### 1. Produce The High-Level Plan First

Start with one reviewable high-level plan.

Include:

- objective
- scope
- assumptions
- major phases or steps
- expected inputs and outputs for each step
- acceptance criteria
- known risks or open questions

Do not start with file-level implementation detail.

### 2. Get Approval Before Expansion

Present the high-level plan for acceptance.

Do not treat any `PLAN_STEP_X.md` file as an active execution plan until the high-level plan is accepted.

**Scratchpad Protocol**: Use temporary scratchpads (like `/tmp/` files or the agent's internal artifact systems) to draft architectures and perform exploratory debugging. Do not write premature implementation details into `PLAN_STEP_X.md` until the approach is validated.

If step files already exist from an older planning pass, replace or remove them until the new high-level plan is accepted.

If scope changes materially, update the high-level plan before changing step contracts.

### 3. Split The Plan Into Step Files

After approval, create step documents such as:

- `PLAN_STEP_01.md`
- `PLAN_STEP_02.md`
- `PLAN_STEP_03.md`

Use zero-padded numbering when order matters.

Make every step independent and complete.

Every step file must define:

- why the step exists
- what inputs it consumes
- what outputs it produces
- what constraints it must respect
- what module tree it introduces or changes
- what public API signatures are exposed at module or feature boundaries
- what boundaries must remain private
- how success is verified
- what public seam each verification method uses when tests are involved

Use `PLAN_STEP_TEMPLATE.md` for the file shape.

### 4. Preserve Stable Step Contracts

Keep each step contract stable:

- declared input data stays the same
- declared output data stays the same
- declared acceptance result stays the same

You may change the internal method while executing the step.

Allowed internal changes:

- reorder files or subtasks
- extract helpers
- change internal sequencing
- replace an internal adapter or service with a better one

Do not do the following without revising the parent plan:

- change required input data
- change promised output data
- move responsibilities across step boundaries in a way that changes the approved flow
- silently broaden step scope

### 5. Adaptation Without Contract Drift

Allow the executing agent to adjust internals when the step contract stays intact.

Allowed without re-approval:

- reorder implementation work inside the step
- add or remove internal helpers
- replace an internal adapter, service, or local abstraction
- narrow a technical tactic that was too broad as long as the promised outputs stay the same

Do not require re-approval for harmless internal cleanup. Over-constraining the step encourages hacks.

Require plan revision before proceeding when any of these would change:

- declared scope
- ownership boundary
- public input or output contract
- acceptance criteria

## Required Step Sections

Every `PLAN_STEP_X.md` must include:

1. `Goal`
2. `Inputs`
3. `Outputs`
4. `Module Tree`
5. `Scope`
6. `Out of Scope`
7. `Constraints`
8. `Implementation Notes`
9. `Verification`
10. `Completion Criteria`
11. `Handoff Notes`

## Module Tree Requirement

Every step must include a module tree when the step creates, moves, removes, or reshapes code structure.

That tree must show:

- the relevant directories, packages, or modules in scope
- the intended public seams
- exposed public API signatures at those seams
- boundaries that must stay internal

The goal is to make structure explicit before implementation starts.

Do not leave the tree implicit when the step changes architecture, module shape, or feature collaboration.

When a step does not change structure, the module tree may be brief, but it should still confirm the unchanged public boundary the step relies on.

## Planning Rules

1. Make every step independently understandable.
2. Make every step verifiable.
3. Preserve the approved input and output contract for every step.
4. Keep each step narrow enough to execute safely and complete enough to be meaningful.
5. Let later steps depend on earlier outputs, but do not let them redefine earlier contracts.
6. If a step reveals a design mistake, revise the high-level plan before changing the step contract.
7. Write the step so the agent can continue without inventing disposable scaffolding.
8. Prefer explicit fallback behavior over vague “figure it out later” instructions.
9. Write steps so different agents would execute them in roughly the same order.
10. State the public seam, private boundaries, and validation path explicitly enough to reduce run-to-run drift.
11. Do not let a plan require verification through private seams.

## Guidance

- prefer stable step boundaries over clever sequencing
- keep plan files focused on execution intent, not speculative implementation detail
- when the task touches architecture, align the plan with `FEATURE.md`, `MODULE.md`, and `REFACTORING.md`
- when a step is complete, make sure its output is usable by the next step without reinterpretation
- state the allowed adaptation space so the agent does not freeze on local implementation details
- state stop-and-ask conditions only for contract, scope, or ownership changes
- if the plan leaves a structural detail unspecified, resolve it through the relevant scoped document instead of inventing a local exception
- use the module tree to make public API exposure and private boundaries visible before code changes start
- structure the step so execution naturally follows: inspect, define target, implement, verify
- describe verification through intended boundaries, and route test-specific rules to `TESTS.md`
