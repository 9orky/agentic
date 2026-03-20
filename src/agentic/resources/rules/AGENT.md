# Agent Rules

Use this file as the entry point for the coding and planning rule set.

Operational usage guidance lives outside `rules/`:

1. `guide/WORKFLOW.md` for how an LLM should use the local `agentic/` folder during a session
2. `guide/COMMANDS.md` for the common `agentic` commands
3. `reference/ARCHITECTURE_MAP.md` for the extracted schema used by the checker

This file exists to route coding work through the right rule documents. It is not the operational handbook for how to use agentic itself.

Do three things here:

1. read the shared rules
2. choose the next document by task scope
3. avoid duplicating general rules in scoped documents

## Reading Order

Read in this order:

1. the project's task manifest, task runner config, or documented command entry point
2. `AGENT.md`
3. `_PROJECT.md` if present

Then route by task:

- planning task: read `PLANNING.md`
- module or file-structure task: read `MODULE.md`
- feature design or feature implementation task: read `FEATURE.md` and `MODULE.md`
- test-writing or verification task: read `TESTS.md` plus the governing feature or module document
- refactor task: read `REFACTORING.md`, then the relevant feature or module guidance

If a feature has a local plan, read it after the shared docs.

## Cross-Doc Quick Matrix

| If the task is mainly about... | Read first | Also read when relevant |
| --- | --- | --- |
| project-specific conventions or exceptions | `_PROJECT.md` | `AGENT.md`, relevant scoped document |
| planning, approval, sequencing | `PLANNING.md` | `FEATURE.md`, `MODULE.md`, `REFACTORING.md` |
| files, directories, public entry points, exports | `MODULE.md` | `FEATURE.md`, `REFACTORING.md`, plan step |
| feature boundary, ownership, collaboration | `FEATURE.md` | `MODULE.md`, `REFACTORING.md`, plan step |
| writing tests, choosing verification seam, fixtures | `TESTS.md` | `FEATURE.md`, `MODULE.md`, `REFACTORING.md` |
| migration, replacement, cleanup | `REFACTORING.md` | `FEATURE.md`, `MODULE.md`, `PLANNING.md` |
| executing an approved plan step | plan step file | `AGENT.md`, plus any scoped document named in step constraints |

Read across the row, not just the first matching cell.

If the task fits more than one row, read all matching rows before acting.

Use the other documents by scope:

- `_PROJECT.md` for project-specific exceptions, naming conventions, and local overrides
- `PLANNING.md` for plan creation, approval, and execution-step breakdown
- `MODULE.md` for directory, file, naming, and module API rules
- `FEATURE.md` for feature composition and feature boundaries
- `TESTS.md` for test strategy, public test seams, and test helper rules
- `REFACTORING.md` for migration and structural change rules

Do not treat every document as equally relevant for every task. Surf to the document that matches the scope.

Keep the shared documents tech-stack agnostic.

If the project needs local exceptions, naming conventions, entry-point conventions, task-runner rules, or allowed architectural deviations, put them in `_PROJECT.md` instead of scattering them across the shared documents.


## Decision Order

Follow this order on every task:

1. identify the task type
2. read the required scoped document
3. identify the owning boundary
4. choose the smallest valid change that satisfies the task
5. execute through the correct public seam
6. verify through the intended boundary
7. update docs if the work exposed a real rule gap or contradiction

No single scoped document is exhaustive.

If a needed instruction is not present in the current scoped document, continue with:

1. this file for shared defaults and precedence
2. `_PROJECT.md` for project-specific exceptions, if present
3. the adjacent scoped document that governs the touched boundary
4. the approved plan if one exists

Absence of a rule in one document is not permission to ignore rules from another relevant document.

## Standard Development Run

Run every development task through the same base sequence.

1. classify the task
2. load the relevant documents
3. inspect the current state only as much as needed (e.g., list directory structure or use file search tools to find consumers before modifying a file; do not read downstream implementation files unless the build or validation step fails)
4. identify the owning boundary and public seam
5. define the target change before editing
6. choose the smallest valid slice that satisfies the task
7. implement without violating boundaries or contracts
8. verify through the intended boundary
9. record plan or doc updates if the work changed the documented understanding

This run shape should stay stable across tasks.

The scoped documents refine this sequence. They do not replace it.

## Minimum Guardrails For Every Task

Before editing, always know:

- the task type
- the owning module or feature
- the public seam being used or changed
- the boundaries that must stay private
- the verification path for the change

Before finishing, always verify:

- scope stayed contained
- public contracts still mean what they say
- boundaries were respected
- the chosen validation path actually ran or was explicitly unavailable


## Precedence Rules

Resolve guidance in this order:

1. explicit user request
2. approved high-level plan and active step contract
3. `_PROJECT.md` for project-specific exceptions and local conventions
4. this document for shared defaults
5. scoped document for the task type
6. current code as behavioral reference only

Always inspect the project's primary package manager configuration, task manifest, or build scripts first to find the authorized test and build commands before attempting to execute standard CLI tools or manual shell scripts.

If two sources conflict, prefer the higher item in the list.

If the conflict would change scope, architecture, or promised outputs, stop and ask.

If the conflict is local and does not change scope or contract, choose the narrowest reversible option and keep moving.

## Shared Rules

1. Keep one owner per concept.
2. Extract repetition only when it improves clarity.
3. Validate once at the correct boundary.
4. Do not use `any`.
5. Stay in scope.
6. Ask before taking an architectural shortcut.
7. Use the project's declared commands or task runner for project tasks.
8. Prefer reversible changes over speculative structure.
9. When information is incomplete, preserve contracts and boundaries first.

## Boundary Rules

1. Treat every directory, package, or equivalent container as a module boundary.
2. Keep each module as independent as practical.
3. Expose the minimal public API through the module's public entry point.
4. Import across module boundaries only through the target module's public entry point.
5. Keep helper types, policies, services, and intermediate models inside the owning module.
6. Keep caller-owned orchestration in the shared parent or root module.
7. Prefer one child-owned seam over multiple imports of child internals.

## Behavioral Rules

1. Treat current callers as behavioral reference, not architectural truth.
2. Treat explicit configuration as explicit behavior. Do not keep unrelated defaults unless the contract says merge.
3. Fail early and loud on invalid input, invalid state, and broken assumptions.
4. Keep guard clauses and failure checks before the happy path. The happy path should read last.
5. Prove boundary behavior through the public API before relying on implementation assumptions.
6. When reality differs from the plan but the contract is unchanged, adapt the implementation and record the decision.
7. When reality differs from the plan and the contract would change, revise the plan before proceeding.

## Default Fallbacks

When the path is ambiguous, use these defaults:

1. keep symbols internal unless a cross-module need is explicit
2. keep orchestration in the caller unless the callee can own one clean seam
3. preserve public input and output contracts even if internals change
4. choose the smallest valid slice instead of creating broad temporary scaffolding
5. ask only when continuing would change approved scope, public contract, or architectural ownership

These defaults are meant to reduce improvisation, not to block progress.

## Scope Routing

Route by question type:

- work decomposition, sequencing, approval: `PLANNING.md`
- files, directories, public entry points, exports: `MODULE.md`
- feature boundary or cooperation between modules: `FEATURE.md`
- verification strategy, test structure, fixtures: `TESTS.md`
- migration, replacement, structural cleanup: `REFACTORING.md`

If the task crosses scopes, read all relevant documents before changing code.

Use these pairings by default:

- planning + architecture: `PLANNING.md` and `FEATURE.md`
- planning + refactor: `PLANNING.md` and `REFACTORING.md`
- feature work: `FEATURE.md` and `MODULE.md`
- feature refactor: `FEATURE.md`, `MODULE.md`, and `REFACTORING.md`
- module change inside a refactor: `MODULE.md` and `REFACTORING.md`

When in doubt, read one additional relevant document before acting.

## Output Rules

- code task: make the change and keep the explanation brief
- documentation task: write the target document directly
- planning task: produce a high-level plan first and split it only after approval

## Similarity Rule

Different tasks may need different scoped documents, but the run should still look similar:

1. route
2. inspect
3. define boundary
4. define target shape
5. implement the smallest valid slice
6. verify
7. report any contract or doc deltas

Prefer predictable runs over ad hoc exploration.