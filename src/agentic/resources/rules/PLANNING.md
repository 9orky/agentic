# Planning

Use this document to create, approve, and expand plans.

## Flow

1. Produce one high-level plan for approval.
2. Do not create active step files before that plan is accepted.
3. After approval, split the plan into zero-padded `PLAN_STEP_XX.md` files.
4. Replace or remove stale step files from older planning passes.

## High-Level Plan

Keep the plan at the boundary and contract level.

Include:

- objective
- scope
- active feature anatomy for the current project
- owning enclosure, public boundary, and public seam
- affected features and the owning part of each touched responsibility
- intended dependency direction across touched parts
- assumptions
- major phases or steps
- expected inputs and outputs for each step
- acceptance criteria
- known risks or open questions
- upstream and downstream dependencies when they affect ownership or sequencing

Resolve material ambiguity with the user before locking the plan.

Do not leave placement implicit. If a touched responsibility cannot be placed clearly in the governing feature anatomy, the plan is not ready.

If the project clearly follows a different anatomy from the shared default and the local docs do not define it, the first plan outcome is to document or confirm that anatomy before structural refactoring.

## Step Contract Rules

1. Preserve approved inputs, outputs, and acceptance criteria.
2. Make each step end to end, verifiable, and narrow enough to execute safely.
3. Name owner, enclosure, public boundary, public seam, scope, and out-of-scope area explicitly.
4. Name the owning part of each touched responsibility explicitly.
5. State the allowed dependency direction for the touched parts explicitly.
6. End each step file with a `Files Tree` section.
7. In the `Files Tree`, annotate each file with its owning part.
8. If the step moves code between structural parts, state the intended source and target ownership.
9. Under the shared default, do not preserve or introduce root buckets such as `contracts`, `ports`, `adapters`, `services`, `types`, or `utils`.
10. Let later steps depend on earlier outputs, but not redefine earlier contracts.
11. Internal sequencing and helper extraction are fine while the contract stays intact and ownership stays explicit.
12. Revise the plan before changing scope, ownership, enclosure boundaries, structural ownership, dependency direction, public contracts, or acceptance criteria.
13. Cross-boundary fixes require a plan amendment or explicit approval.

## Step File Template

Required sections:

- `Goal`
- `Inputs`
- `Outputs`
- `Scope`
- `Out of Scope`
- `Constraints`
- `Layer Ownership`
- `Dependency Direction`
- `Execution Order`
- `Allowed Adaptations`
- `Stop And Ask If`
- `Implementation Notes`
- `Decision Log`
- `Verification`
- `Completion Criteria`
- `Handoff Notes`
- `Files Tree`

`Files Tree` must be the final section. Keep it concise and include only relevant signatures, owning parts, and short notes.

## Guidance

1. Prefer stable step boundaries over clever sequencing.
2. Keep plan files focused on execution intent, not speculative detail.
3. Align architecture-sensitive plans with `FEATURE.md`, `MODULE.md`, and `REFACTORING.md`.
4. Use `FEATURE.md` as the default source of truth unless a repo-local override replaces it.
5. Resolve file placement during planning, not during implementation.
6. If a file or type does not fit clearly in one owning part, stop and tighten the plan before coding.
7. Make each completed step usable by the next step without reinterpretation.
8. Once `Files Tree` captures the involved files, owning parts, signatures, and short notes, remove repeated file-path and boundary prose unless it adds new contract information.
9. Plan around preserving or strengthening the owning enclosure so the feature may grow internally without spreading responsibilities, seams, or coordination outside it.