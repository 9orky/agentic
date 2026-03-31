# agentic

`agentic` is a pipx-first CLI for bootstrapping a project-local architecture contract that both humans and agents can read.

The installed package gives you the command surface.

The generated `agentic/` folder gives a project a durable collaboration surface: shared rules, local extensions, and the architecture config that `agentic check` validates.

## What It Ships

The packaged rules are organized as a navigable documentation tree rather than one flat bundle of long files.

That shape exists so an agent can build only the context it needs:

1. start at `AGENT.md`
2. route to the governing rule-set bootstrap file
3. descend only into the narrower documents required by the task

The shared source of truth for that tree lives under `src/agentic/resources/rules/`.

Use [src/agentic/resources/README.md](src/agentic/resources/README.md) to obtain the operating guidance for maintaining the packaged rules tree.

The runtime contract that gets bootstrapped into a target project is generated from those packaged resources.

## Navigable Rules

The rules are split by concern.

Current top-level flow:

1. `AGENT.md` is the global router.
2. Each rule set has its own folder and its own bootstrap file.
3. Detailed constraints live below that bootstrap layer.

Example discovery path:

1. planning work starts in `planning/PLANNING.md`
2. material domain modeling stays within the planning guides and the affected plan files

This keeps the read path short and inspectable. The agent does not need to load unrelated rule files to plan or refactor one narrow slice of work.

## Architecture Check

Use the feature guide below to obtain the architecture-check configuration model, matching semantics, and checker behavior:

- [src/agentic/features/architecture_check/README.md](src/agentic/features/architecture_check/README.md)

That guide is the place for checker details. This README stays focused on what agentic is and how its rule system is organized.

## Project Idea

`agentic` is not just a tool surface. It is a system for deterministic cooperation with LLM coding agents.

It gives the agent a predictable way to discover only the context it needs, in the order it needs it, so the next action is constrained by shared rules instead of guesswork.

It gives the human a faster way to inspect whether the agent is following the intended path, because the reasoning surface is externalized into a visible project contract rather than hidden inside the model.

The goal is simple: make collaboration with coding agents more inspectable, more repeatable, and therefore more trustworthy.
