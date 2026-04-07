# Project Overview

`agentic` is a CLI for bootstrapping and maintaining a project-local collaboration contract that both humans and coding agents can inspect.

## Why The Project Exists

Collaboration with coding agents often fails because the working contract is too implicit. Architecture boundaries, expected read order, and project-specific conventions are spread across code, habit, and prompt state.

`agentic` tries to make that contract visible.

It does that by combining:

- packaged shared assets that ship with the tool
- a generated project-local contract inside the target repository
- an architecture agreement that can be checked against the codebase

## What The Product Gives You

The installed package gives you the runtime and CLI surface.

The generated `agentic/` folder gives the target project a durable collaboration surface:

- mirrored packaged shared rules
- a repo-local profile surface under `agentic/rules/local/`
- a checked architecture config

## Human And Agent Value

For agents, the value is constrained discovery. The generated `agentic/` folder is the primary operating boundary, so guidance is externalized into a predictable project surface rather than left entirely inside hidden prompt state.

For humans, the value is inspectability. The collaboration contract becomes visible as files, config, and runtime checks that can be reviewed in the repository.

## Related Docs

- [getting-started.md](/Users/gorky/Projects/agentic/docs/project/getting-started.md) for first-use flow
- [../runtime/workspace-contract.md](/Users/gorky/Projects/agentic/docs/runtime/workspace-contract.md) for generated contract behavior
- [../runtime/architecture-check.md](/Users/gorky/Projects/agentic/docs/runtime/architecture-check.md) for architecture-check behavior
- [../maintainers/rule-system.md](/Users/gorky/Projects/agentic/docs/maintainers/rule-system.md) for maintainership details about rules and the local profile model

## Source Inputs

- [README.md](/Users/gorky/Projects/agentic/README.md)

## Boundary

Write this page as project documentation. Do not turn it into a rule router or a description of packaged rule metadata.