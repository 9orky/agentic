# Plan Step Template

Use this file shape for every `PLAN_STEP_XX.md` document.

Keep the step self-contained. Do not change the declared inputs, outputs, or completion contract without first updating the approved high-level plan.

Use this template to make execution deterministic without locking the implementation into brittle tactics.

This template does not replace the scoped rule documents.

If a step changes module boundaries, feature boundaries, or refactor structure, list the applicable companion documents in `Constraints` and follow them during execution.

Silence in the step file is not permission to ignore a relevant rule from `AGENT.md`, `MODULE.md`, `FEATURE.md`, or `REFACTORING.md`.

The step should be written so different agents would execute it in a similar order.

## Goal

State the concrete result this step must achieve.

## Inputs

List the exact inputs this step consumes.

- source documents
- source files or modules
- approved decisions
- required data or interfaces

## Outputs

List the exact outputs this step must produce.

- changed files
- new files
- preserved contracts
- verification artifacts

## Module Tree

Describe the relevant module tree for this step.

Include:

- directories, packages, and modules in scope
- public seams exposed by module entry points or feature boundaries
- exposed public API signatures at those seams
- boundaries that must remain internal

Use a compact tree plus signatures, for example:

```text
src/features/example/
	public-entry
		exposes ExampleFeatureBoundary
	example-feature
		public execute(input: ExampleInput): ExampleOutput
	services/
		scoring-service
			internal only
```

If the step does not change structure, state the existing module tree that remains in force.

## Scope

State what this step is allowed to change.

## Out of Scope

State what this step must not change.

## Constraints

List the rules this step must respect.

- boundary rules
- module rules
- feature rules
- refactoring limits
- compatibility constraints
- companion documents consulted

## Execution Order

List the expected execution sequence for the step.

Use the shared run shape unless the step has a good reason to narrow it:

1. inspect current state
2. confirm boundary and target shape
3. implement the smallest valid slice
4. verify through the intended boundary
5. record any contract-safe tactical decisions

## Allowed Adaptations

List the changes the agent may make without revising the plan.

- internal sequencing changes
- helper extraction
- internal service or adapter replacement
- local cleanup that does not alter the declared contract

Be explicit. If this section is empty, the default is: internal changes are allowed if inputs, outputs, ownership, and acceptance criteria stay stable.

## Stop And Ask If

List the conditions that require a plan update or explicit approval.

- scope change
- contract change
- ownership change
- acceptance criteria change
- irreversible tradeoff outside the approved step

## Implementation Notes

Record the intended execution approach.

Use this section for internal sequencing only. Do not redefine the declared input or output contract here.

## Decision Log

Record step-local decisions that changed the tactic but not the contract.

Keep this brief.

## Verification

List how completion is verified.

- tests
- architecture checks
- build checks
- document consistency checks

If tests are part of verification, name the public interface being exercised and follow `TESTS.md`.

## Completion Criteria

Declare the conditions that make the step done.

1. required outputs exist
2. verification passes
3. scope stayed within contract
4. no forbidden contract drift occurred

## Handoff Notes

State what the next step can now rely on.