# Planning

Use this document to create, approve, and expand plans.

## Flow

1. Produce one high-level plan for approval.
2. Do not create active step files before that plan is accepted.
3. After approval, split the plan into zero-padded `PLAN_STEP_XX.md` files.
4. Replace or remove stale step files from older planning passes.

## High-Level Plan

Keep the plan at the boundary and contract level.

Use a strategic DDD lens before naming phases or files.

Include:

- objective
- scope
- business capability, bounded context, and subdomain being changed
- extracted domain concepts for the change: entities, value objects, domain services, repositories, policies, and events when relevant
- identity, invariants, and lifecycle expectations for each extracted domain concept that materially affects design
- active feature anatomy for the current project
- owning enclosure, public boundary, and public seam
- affected features and the owning part of each touched responsibility
- explicit layer placement for each extracted concept and the reason it belongs there
- application orchestration or use-case coordination required to move the domain behavior
- infrastructure responsibilities required to persist, integrate, or translate external concerns
- ui responsibilities required to collect inputs or present outputs without absorbing business rules
- intended dependency direction across touched parts
- intended layer progression across the work: `domain -> infrastructure -> application -> ui`
- assumptions
- major phases or steps
- expected inputs and outputs for each step
- acceptance criteria
- known risks or open questions
- upstream and downstream dependencies when they affect ownership or sequencing

Resolve material ambiguity with the user before locking the plan.

Do not leave placement implicit. If a touched responsibility cannot be placed clearly in the governing feature anatomy, the plan is not ready.

If the project clearly follows a different anatomy from the shared default and the local docs do not define it, the first plan outcome is to document or confirm that anatomy before structural refactoring.

## Strategic Domain Modeling

Before locking a high-level plan, describe the domain in business language, not file names.

1. Name the bounded context or business slice being changed.
2. Extract the candidate concepts implied by the request and current behavior.
3. Classify each concept as an entity, value object, domain service, repository, policy, event, application coordinator, infrastructure adapter, or ui contract.
4. For each concept, state its identity, invariants, lifecycle, and owning layer.
5. If a concept cannot be classified or placed deterministically, stop and tighten the model before planning steps.
6. Prefer promoting stable business rules into explicit domain concepts instead of leaving them buried in orchestration code or adapters.
7. Keep tactical DDD terms honest. Do not invent entities, services, or repositories unless they improve ownership clarity and behavior.

Under the shared default anatomy, use this placement model unless a repo-local override replaces it:

1. `domain`: entities, value objects, aggregates, domain services, domain policies, specifications, and repository contracts that are part of the business language or protect domain invariants.
2. `application`: use cases, workflow coordination, command-query handling, transaction boundaries, cross-feature coordination, and outward capability abstractions used to execute a use case.
3. `infrastructure`: repository implementations, persistence mappings, framework adapters, filesystem or network clients, and external service integrations.
4. `ui`: delivery-specific request and response models, input parsing, presentation formatting, command binding, and validation that exists because of the delivery surface rather than the business model.

If repository ownership is ambiguous, resolve it explicitly:

1. Put the repository contract in `domain` when it expresses how the business model is loaded, stored, or queried in domain language.
2. Put the abstraction in `application` when it exists only as an execution dependency of a use case and does not belong to the domain vocabulary.
3. Put concrete adapters and mappers in `infrastructure`.

If the shared default feature layout governs, also plan the feature with these modeling constraints unless a repo-local override replaces them:

1. Feature layers use classes only.
2. Free functions are forbidden in feature layers.
3. One class per file is mandatory in feature layers.
4. If a planned concept cannot justify a class, it likely belongs in another layer or the model needs to be tightened.
5. If one-class-per-file would be violated inside an anchor, plan the anchor in package form explicitly.

If the shared default domain layout governs, also plan the domain with these stricter constraints unless a repo-local override replaces them:

1. Domain uses classes only.
2. Free functions are forbidden in domain.
3. One class per file is mandatory in domain.
4. If a planned domain concept cannot justify a class, it likely belongs in another layer or the model needs to be tightened.
5. Required domain anchors may be implemented as files or same-named packages.
6. If more than one domain class is expected inside one anchor, plan that anchor in package form explicitly.
7. Every planned domain class must map to exactly one anchor: `entity`, `value_object`, `service`, or `repository` when present.
8. Do not leave domain classes loose under `domain/` outside those anchors.

For any layer whose layout names anchors, also plan the anchor form explicitly when that decision affects code shape:

1. State whether each touched anchor will stay in file form or move to same-named package form.
2. If an anchor needs multiple owned implementation files, plan package form rather than loose sibling helpers.
3. Keep the anchor name stable across the plan and implementation.
4. If package form is chosen, treat the anchor `__init__.py` as the export seam and place implementation behind it.
5. Under the shared default application layout, plan all application-owned files behind `commands`, `queries`, and optional `services` or `adapters`; do not plan loose files directly under `application/` other than the layer shim.

For any touched cross-layer dependency, also plan the layer shim explicitly:

1. State which shim the consumer layer will import from.
2. Do not plan deep imports from another layer's internal files.
3. If a required symbol is missing, add it to the target layer shim in the plan rather than bypassing the shim.

## Step Contract Rules

1. Preserve approved inputs, outputs, and acceptance criteria.
2. Make each step end to end, verifiable, narrow enough to execute safely, and owned by exactly one layer.
3. Name owner, enclosure, public boundary, public seam, scope, and out-of-scope area explicitly.
4. Name the owning part of each touched responsibility explicitly.
5. State the allowed dependency direction for the touched parts explicitly.
6. State which domain concepts are created, changed, moved, or intentionally left unchanged in the step.
7. If introducing a repository, name the owner of the abstraction and the owner of the concrete adapter separately.
8. Order implementation steps by layer unless the user explicitly approves a different sequence: `domain`, then `infrastructure`, then `application`, then `ui`.
9. Do not mix unfinished work from multiple layers inside one step.
10. A step is not complete if its owning layer still depends on placeholders, stubs, fake wiring, TODO branches, or deferred contracts for that layer.
11. A step is only complete when the owning layer is internally coherent, wired to the already-approved lower layers it depends on, and ready for the next layer to build on it without reinterpretation.
12. Include a detailed implementation tree for the step with files, classes, functions, and relevant signatures.
13. End each step file with a `Files Tree` section.
14. In the `Files Tree`, annotate each file with its owning part.
15. If the step moves code between structural parts, state the intended source and target ownership.
16. Under the shared default, do not preserve or introduce root buckets such as `contracts`, `ports`, `adapters`, `services`, `types`, or `utils`.
17. Let later steps depend on earlier outputs, but not redefine earlier contracts.
18. Internal sequencing and helper extraction are fine while the contract stays intact and ownership stays explicit.
19. Revise the plan before changing scope, ownership, enclosure boundaries, structural ownership, dependency direction, public contracts, or acceptance criteria.
20. Cross-boundary fixes require a plan amendment or explicit approval.

## Step Sequencing Model

Use this default sequencing model for implementation steps unless a repo-local override replaces it or the user explicitly approves an exception.

1. `domain`: define or reshape the business model, invariants, policies, repository contracts, and pure domain behavior.
2. `infrastructure`: implement adapters required to support the approved domain model, including persistence, external clients, and mappings.
3. `application`: wire use cases, orchestration, transactions, and cross-feature coordination against completed domain and infrastructure capabilities.
4. `ui`: bind delivery, input parsing, presentation, and command or endpoint seams on top of completed lower layers.

Sequencing constraints:

1. Do not start a higher-layer implementation step while the lower layer it depends on is still conceptually unresolved.
2. A later layer may reference contracts from earlier approved steps, but it must not redefine them implicitly.
3. If a higher layer reveals a missing lower-layer concept, amend the plan and return to the owning layer rather than patching around the gap.
4. A step may touch lower layers only to consume already-approved seams, not to reopen their design silently.

## Step File Template

Required sections:

- `Goal`
- `Inputs`
- `Outputs`
- `Scope`
- `Out of Scope`
- `Constraints`
- `Domain Model Impact`
- `Owning Layer`
- `Layer Ownership`
- `Dependency Direction`
- `Execution Order`
- `Allowed Adaptations`
- `Stop And Ask If`
- `Implementation Notes`
- `Detailed Implementation Tree`
- `Decision Log`
- `Verification`
- `Completion Criteria`
- `Handoff Notes`
- `Files Tree`

`Files Tree` must be the final section. Keep it concise and include only relevant signatures, owning parts, and short notes.

`Detailed Implementation Tree` must describe the concrete implementation slice expected from the step. Include planned files, classes, dataclasses, protocols, functions, and public method signatures that materially define the step outcome. Use it to make the step executable without guessing structure during coding.

## Guidance

1. Prefer stable step boundaries over clever sequencing.
2. Keep plan files focused on execution intent, not speculative detail.
3. Align architecture-sensitive plans with `FEATURE.md`, `MODULE.md`, and `REFACTORING.md`.
4. Use `FEATURE.md` as the default source of truth unless a repo-local override replaces it.
5. Write the plan in business language first, then map the result to layers, files, and seams.
6. Resolve file placement during planning, not during implementation.
7. Plan steps so each one belongs to exactly one layer and leaves that layer complete enough for the next layer to proceed without placeholders.
8. If a file or type does not fit clearly in one owning part, stop and tighten the plan before coding.
9. Use explicit `belongs in X because Y` statements when a concept could plausibly land in more than one layer.
10. Prefer deterministic names such as `OrderId value object in domain` or `SyncProject use case in application` over generic placeholders.
11. Treat placeholder-based progress as plan failure for the owning layer unless the user explicitly approves an interim seam.
12. Make each completed step usable by the next step without reinterpretation.
13. Use the detailed implementation tree to remove ambiguity about concrete code shape before coding starts.
14. Once `Files Tree` captures the involved files, owning parts, signatures, and short notes, remove repeated file-path and boundary prose unless it adds new contract information.
15. Plan around preserving or strengthening the owning enclosure so the feature may grow internally without spreading responsibilities, seams, or coordination outside it.
16. When layer-layout docs define a minimum layout, plan for those anchors as the baseline shape, not as an upper bound. Add internal modularity inside the owning layer when scale or isolation requires it.
17. When the shared default domain rules govern, plan domain files as class-based slices: no free functions and one class per file.
18. When one-class-per-file and anchor-based layout would conflict, plan the anchor as a package rather than weakening either rule.
19. When non-domain layer anchors need more than one owned implementation file, plan those anchors as same-named packages rather than scattering loose helpers around the layer.
20. Under the shared default application layout, place application models, use cases, orchestration helpers, and capability abstractions inside `commands`, `queries`, `services`, or `adapters` according to ownership; do not leave them loose at the `application/` root.
21. Plan every cross-layer import through the target layer shim; deep cross-layer imports are plan failure.