# Step Planning Rules

Document Class: leaf

## Purpose

Use this file to define executable step contracts after a high-level plan is accepted.

## Applies When

Use this file after a high-level plan is accepted and the work is being split into executable steps.

## Scope

Executable step files must be named `PLAN_STEP_0X.md` in the order they are intended to run.
Executable step files must live at the same directory level as their owning `PLAN.md`.
Do not place step files in nested planning subdirectories.

## Core Rules

1. Preserve approved inputs, outputs, and acceptance criteria.
2. Make each step narrow, end to end, verifiable, and owned by exactly one layer.
3. Name owner, enclosure, public boundary, public seam, scope, and out-of-scope area explicitly.
4. State the allowed dependency direction for the touched parts explicitly.
5. State which domain concepts are created, changed, moved, or intentionally left unchanged.
6. If introducing a repository, name the owner of the abstraction and the owner of the concrete adapter separately.
7. Do not mix unfinished work from multiple layers inside one step.
8. Each step file must show the target files tree for that step clearly enough that the intended file names and owned responsibilities are visible before implementation starts.
9. After completing a step, check the code against both the approved high-level plan and the active step file, then update the step file if the verified implementation differs in a still-approved way.
10. After the last step, run one final alignment check across the code, the high-level plan, and the full step set.

### Sequencing Model

Default implementation order:

1. `domain`
2. `infrastructure`
3. `application`
4. `ui`

If a higher layer reveals a missing lower-layer concept, amend the plan and return to the owning layer instead of patching around the gap.

## Constraints

### Required Sections

Each step file must include:

1. `Goal`
2. `Inputs`
3. `Outputs`
4. `Scope`
5. `Out of Scope`
6. `Constraints`
7. `Domain Model Impact`
8. `Owning Layer`
9. `Layer Ownership`
10. `Dependency Direction`
11. `Execution Order`
12. `Allowed Adaptations`
13. `Stop And Ask If`
14. `Implementation Notes`
15. `Detailed Implementation Tree`
16. `Decision Log`
17. `Verification`
18. `Completion Criteria`
19. `Handoff Notes`
20. `Files Tree`

`Files Tree` must be the final section.

`Files Tree` is the target files tree for the step. It must show the planned file names and owning responsibilities so the intended implementation shape is reviewable before coding.

### Step Lifecycle

For each approved step:

1. implement the step through the owning layer
2. verify the code against the active step file
3. verify the code still aligns with the approved high-level plan
4. update the step file if the verified implementation changed in a way that remains within approved scope

After the final step:

1. run a final alignment check across the codebase, the approved high-level plan, and all `PLAN_STEP_0X.md` files
2. resolve any drift or record the approved final state in the relevant plan files

## If Ambiguous, Go To

### Layer Routing

When a step needs layer-specific constraints, read only the matching file under `rules/feature/module/layers/`.

## Acceptance Check

1. Each step is narrow, end to end, verifiable, and owned by exactly one layer.
2. Each step file contains the required sections, with `Files Tree` last.
3. The implementation order respects the approved plan and layer ownership.
4. Step execution includes verification against both the active step file and the approved high-level plan.