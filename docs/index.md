# Documentation

This `docs/` tree is the human-facing documentation surface for the `agentic` project.

It is not part of the packaged rule corpus. Agents should not treat `docs/` as governing rule input in the same way as `src/agentic/resources/rules/` or the generated workspace rule contract under `agentic/`.

## Purpose

- Explain what `agentic` is and how the project is organized.
- Document runtime behavior such as workspace contract bootstrapping and architecture checks.
- Capture maintainer guidance that should be readable as project documentation rather than embedded only in routing rules or code.

## Sections

- [project/overview.md](/Users/gorky/Projects/agentic/docs/project/overview.md): project framing, goals, and collaboration model
- [project/getting-started.md](/Users/gorky/Projects/agentic/docs/project/getting-started.md): install, CLI entrypoints, and first-use flow
- [runtime/workspace-contract.md](/Users/gorky/Projects/agentic/docs/runtime/workspace-contract.md): generated project contract and sync behavior
- [runtime/architecture-check.md](/Users/gorky/Projects/agentic/docs/runtime/architecture-check.md): architecture-check feature behavior and config entrypoints
- [maintainers/packaged-resources.md](/Users/gorky/Projects/agentic/docs/maintainers/packaged-resources.md): what ships under packaged resources and how it is consumed
- [maintainers/rule-system.md](/Users/gorky/Projects/agentic/docs/maintainers/rule-system.md): packaged rule model and workspace-local extension model
- [maintainers/validation-scope.md](/Users/gorky/Projects/agentic/docs/maintainers/validation-scope.md): current `check-rules` / `check-rule-schema` scope and limitations
- [architecture/mapping.md](/Users/gorky/Projects/agentic/docs/architecture/mapping.md): maintained architecture mapping for the current repo

## Boundary

- `docs/` explains the project.
- `src/agentic/resources/rules/` defines packaged rule assets.
- `agentic/` is the generated live operating contract surface, including `agentic/rules/local/` for repo-specific narrowing.

If a page belongs to `docs/`, write it as project documentation. Do not write it as a rule router, policy document, or execution artifact for agents.

## Migration Map

- Product summary stays in `README.md` as the landing page.
- Rule-system explanation moves to [maintainers/rule-system.md](/Users/gorky/Projects/agentic/docs/maintainers/rule-system.md) and [runtime/workspace-contract.md](/Users/gorky/Projects/agentic/docs/runtime/workspace-contract.md).
- Architecture-check explanation moves to [runtime/architecture-check.md](/Users/gorky/Projects/agentic/docs/runtime/architecture-check.md).
- Broader project framing moves to [project/overview.md](/Users/gorky/Projects/agentic/docs/project/overview.md).
- First-use and command-surface guidance moves to [project/getting-started.md](/Users/gorky/Projects/agentic/docs/project/getting-started.md).

- The maintained architecture map now lives at [architecture/mapping.md](/Users/gorky/Projects/agentic/docs/architecture/mapping.md).
- The legacy page now exists only as a redirect note because its content had drifted into an architecture-check guide.

## Working Assumptions

- The repository root keeps `README.md` plus active planning artifacts; substantive project docs move under `docs/`.
- The docs roadmap may mention a future workspace-contract summary command only as a possible future enhancement, not as a current feature.
- Automated doc-link verification is desirable but remains optional until Step 04 decides whether the current test surface can support it cheaply.