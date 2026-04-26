# Getting Started

This page covers the normal first-use flow for the `agentic` CLI.

## Main Commands

- `agentic`: bootstrap the current directory using the default `init` path
- `agentic init --project-root <path>`: create the project-local contract
- `agentic update --project-root <path>`: refresh mirrored packaged assets in an existing project contract
- `agentic architecture check --project-root <path>`: run the architecture check
- `agentic architecture hotspots --project-root <path>`: inspect risky files in the architecture graph
- `agentic architecture summary --project-root <path>`: get a short agent-facing reading order and risk briefing
- `agentic check-rule-schema`: validate the packaged markdown rule contract

## First Bootstrap Flow

1. Run `agentic` or `agentic init` in the target repository.
2. Review the generated `agentic/agentic.yaml`, mirrored shared rules, and the local profile surface under `agentic/rules/local/`.
3. Keep repo-specific narrowing under `agentic/rules/local/` when shared guidance is not enough.
4. Run `agentic architecture check` to validate the architecture agreement against the current codebase.

## Update Flow

Use `agentic update` when packaged shared assets need to be refreshed in an existing project contract.

Current behavior is conservative:

- packaged shared files can be updated
- existing local workspace files under `agentic/rules/local/` are preserved
- the command reports created, updated, and preserved files

## Read Next

- [../runtime/workspace-contract.md](/Users/gorky/Projects/agentic/docs/runtime/workspace-contract.md) for the generated contract model
- [../runtime/architecture-check.md](/Users/gorky/Projects/agentic/docs/runtime/architecture-check.md) for architecture runtime behavior and config guidance
- [../index.md](/Users/gorky/Projects/agentic/docs/index.md) for the full docs hub

## Source Inputs

- [README.md](/Users/gorky/Projects/agentic/README.md)
- [src/agentic/cli.py](/Users/gorky/Projects/agentic/src/agentic/cli.py)

## Boundary

Keep this page focused on operator-facing usage. The generated `agentic/` folder is the live operating contract; deep runtime semantics belong in the runtime docs section.
