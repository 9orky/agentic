# agentic

`agentic` is a pipx-first CLI for bootstrapping a project-local architecture contract that both humans and agents can read.

Project documentation lives under [docs/INDEX.md](/Users/gorky/Projects/agentic/docs/INDEX.md). That docs tree explains the project and its runtime behavior to humans; it is not part of the packaged rule corpus under `src/agentic/resources/rules/`.

The installed package gives you the command surface. The generated `agentic/` folder gives a target repository a durable collaboration contract: packaged shared rules, workspace-local extensions, and the architecture config that `agentic check` validates.

## Core Commands

- `agentic`: bootstrap the current directory using the default `init` behavior
- `agentic init`: create the project-local contract
- `agentic update`: refresh mirrored packaged assets while preserving local workspace additions
- `agentic check`: run the architecture check using the project config
- `agentic hotspots`: inspect import hotspot counts from the dependency graph
- `agentic check-rule-schema`: validate the packaged markdown rule corpus

## Documentation

- [docs/project/overview.md](/Users/gorky/Projects/agentic/docs/project/overview.md): what the project is and why it exists
- [docs/project/getting-started.md](/Users/gorky/Projects/agentic/docs/project/getting-started.md): installation assumptions and first-use flow
- [docs/runtime/workspace-contract.md](/Users/gorky/Projects/agentic/docs/runtime/workspace-contract.md): generated contract behavior and sync model
- [docs/runtime/architecture-check.md](/Users/gorky/Projects/agentic/docs/runtime/architecture-check.md): architecture-check behavior and config guidance
- [docs/maintainers/rule-system.md](/Users/gorky/Projects/agentic/docs/maintainers/rule-system.md): packaged rules versus workspace-local additions
- [docs/maintainers/validation-scope.md](/Users/gorky/Projects/agentic/docs/maintainers/validation-scope.md): what current rule-schema validation does and does not check

## Project Idea

`agentic` is not just a tool surface. It is a system for deterministic cooperation with LLM coding agents.

It gives the agent a predictable way to discover only the context it needs, in the order it needs it, so the next action is constrained by shared rules instead of guesswork.

It gives the human a faster way to inspect whether the agent is following the intended path, because the reasoning surface is externalized into a visible project contract rather than hidden inside the model.

The goal is simple: make collaboration with coding agents more inspectable, more repeatable, and therefore more trustworthy.
