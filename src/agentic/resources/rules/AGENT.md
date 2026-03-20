# Agent Rules

Use this file as the routing hub for the shared rules.

Shared docs live under `rules/*.md`.
Local changes belong only in:

- `rules/overrides/` for repo-local replacements of shared docs
- `rules/project-specific/` for new repo-local rules

## Reading Order

1. Read the project's task runner, manifest, or documented entry point.
2. Read `AGENT.md`.
3. Read the governing doc for the task.
4. Read matching files in `rules/overrides/`.
5. Read relevant files in `rules/project-specific/`.

Route by task:

- planning: `PLANNING.md`
- module shape or public API: `MODULE.md`
- feature ownership or collaboration: `FEATURE.md`, then `MODULE.md`
- testing or verification: `TESTS.md` plus the governing feature or module doc
- refactor or migration: `REFACTORING.md` plus the governing feature or module doc
- approved plan step: the step file plus docs named in `Constraints`

If the task crosses scopes, read all matching docs.

## Active Feature Anatomy

For feature work, resolve the governing feature anatomy first.

1. Start with the shared default in `FEATURE.md`.
2. If a file in `rules/overrides/` or `rules/project-specific/` replaces it, the local anatomy governs.
3. If the code shows a stable different anatomy but the docs do not define it, stop before structural refactoring and get that anatomy documented.

## Shared Defaults

1. Keep one owner per concept.
2. Follow the governing feature anatomy with the same strictness whether it is shared or repo-local.
3. Do not introduce structure that violates the governing feature anatomy.
4. Add structure only when complexity requires it, unless a governing doc requires it.
5. Expose the minimum public boundary through the minimum public seam.
6. Cross boundaries only through the target boundary's public seam.
7. Preserve feature enclosures.
8. Preserve explicit inputs and outputs unless the user or approved plan changes them.
9. Verify through the intended public boundary and public seam.
10. Use the project's declared commands or task runner.
11. Stay in scope. Stop and ask before changing scope, ownership, or a public contract.
12. After two failed attempts on the same boundary or tactic, stop and ask.
13. Do not add summaries unless the user explicitly asks for one.
14. Do not add comments in code.
15. Prefer silent execution: code first, speak only when the user needs a decision, blocker, or verification result.

## Standard Run

1. Classify the task.
2. Load the governing docs.
3. Resolve the active feature anatomy.
4. Inspect only the needed context.
5. Identify owner, enclosure, public boundary, and public seam.
6. Define the smallest valid change.
7. Implement through the correct boundary.
8. Verify through the intended public boundary and public seam.
9. Record any plan or doc delta if understanding changed.

## Guardrails

Before editing, know:

- task type
- owner
- active feature anatomy
- enclosure being preserved
- owning part of each touched responsibility
- allowed dependency direction across touched parts
- public boundary and public seam
- private boundaries that must stay private
- verification path

Before finishing, verify:

- scope stayed contained
- enclosure stayed intact
- no touched file escaped the governing feature anatomy
- no project-default mismatch was introduced by assuming the wrong anatomy
- dependency direction still matches the governing rules
- public contracts still mean what they say
- boundaries were respected
- the intended validation path ran or was explicitly unavailable

## Precedence

Use this order:

1. explicit user request
2. approved plan and active step contract
3. relevant override file
4. relevant project-specific file
5. core doc for the task
6. current code as behavioral reference only

If a conflict would change scope, ownership, or a promised output, stop and ask. Otherwise choose the narrowest reversible option.

If local docs replace the shared default feature anatomy, the local docs govern.

If current code conflicts with the governing documented feature anatomy, treat the code as refactor input, not as architectural authority.

## Rule Maintenance

1. Keep shared reusable rules in the shared docs.
2. Do not edit local core docs; they are update-owned.
3. Put repo-local replacements of shared docs in `rules/overrides/`.
4. Put new repo-local rules in `rules/project-specific/`.
5. Do not fork the same rule across multiple documents.