# Step Planning Rules

Use this file after a high-level plan is accepted and the work is being split into executable steps.

## Core Rules

1. Preserve approved inputs, outputs, and acceptance criteria.
2. Make each step narrow, end to end, verifiable, and owned by exactly one layer.
3. Name owner, enclosure, public boundary, public seam, scope, and out-of-scope area explicitly.
4. State the allowed dependency direction for the touched parts explicitly.
5. State which domain concepts are created, changed, moved, or intentionally left unchanged.
6. If introducing a repository, name the owner of the abstraction and the owner of the concrete adapter separately.
7. Do not mix unfinished work from multiple layers inside one step.

## Sequencing Model

Default implementation order:

1. `domain`
2. `infrastructure`
3. `application`
4. `ui`

If a higher layer reveals a missing lower-layer concept, amend the plan and return to the owning layer instead of patching around the gap.

## Required Sections

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

## Layer Routing

When a step needs layer-specific constraints, read only the matching file under `rules/feature/layers/`.