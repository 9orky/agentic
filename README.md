# agentic

[![PyPI version](https://img.shields.io/pypi/v/agentic.svg)](https://pypi.org/project/agentic/)
[![Python versions](https://img.shields.io/pypi/pyversions/agentic.svg)](https://pypi.org/project/agentic/)
[![CI](https://img.shields.io/github/actions/workflow/status/9orky/agentic/ci.yml?branch=main&label=ci)](https://github.com/9orky/agentic/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](https://github.com/9orky/agentic/blob/main/LICENSE)

Coding agents are fast. Chaos is faster.

`agentic` is a `pipx`-first CLI for teams who want something better than "just let the model vibe with the repo and see what happens."

It bootstraps a project-local contract that both humans and agents can read, then uses that contract to keep architecture work more inspectable, more repeatable, and a lot less mystical.

There are no silver bullets here. Just fewer unforced errors.

## What it does

`agentic` gives a repository three useful things:

- a generated local contract under `agentic/`
- packaged shared rules that can be mirrored and updated
- architecture analysis that helps an agent understand where the codebase is risky before it starts "helping"

That means you can:

- initialize a repo with a durable collaboration surface
- refresh shared guidance without trampling local additions
- validate architecture boundaries
- rank risky files by dependency pressure and public surface
- generate a short reading order for an agent before edits begin

## Install

```bash
pipx install agentic
```

If you prefer to poke it first:

```bash
pipx run agentic --help
```

## Quick start

```bash
agentic init
agentic architecture check --project-root .
agentic architecture hotspots --project-root .
agentic architecture summary --project-root .
```

After `init`, your repo gets an `agentic/` directory with:

- `agentic/agentic.yaml` for architecture rules
- `agentic/rules/` for mirrored shared guidance
- `agentic/rules/local/` for project-specific narrowing
- `agentic/code/` for local generation recipes

## Core commands

- `agentic`
  Bootstrap the current directory using the default `init` path.
- `agentic init`
  Create the local contract surface.
- `agentic update`
  Refresh packaged assets while preserving local workspace additions.
- `agentic architecture check`
  Validate the repository against the architecture agreement.
- `agentic architecture hotspots`
  Rank risky files by imports, public surface, and implementation size.
- `agentic architecture summary`
  Produce an agent-facing reading order and risk briefing.
- `agentic check-rule-schema`
  Validate the packaged markdown rule corpus.

## Why this exists

Most teams do not actually have an "AI adoption problem."

They have a clarity problem.

The agent does not know what matters first, what is stable, what is sacred, what is local convention, what is temporary, or which files are about to explode into a week of cleanup if touched casually.

`agentic` externalizes that context into something visible.

So instead of asking a coding agent to be telepathic, you give it a map, a contract, and a few guardrails.

That turns collaboration from folklore into a system.

## Documentation

- [Getting started](https://github.com/9orky/agentic/blob/main/docs/project/getting-started.md)
- [Workspace contract runtime](https://github.com/9orky/agentic/blob/main/docs/runtime/workspace-contract.md)
- [Architecture runtime](https://github.com/9orky/agentic/blob/main/docs/runtime/architecture-check.md)
- [Repository architecture map](https://github.com/9orky/agentic/blob/main/docs/architecture/mapping.md)
- [Rule system notes](https://github.com/9orky/agentic/blob/main/docs/maintainers/rule-system.md)

## Release notes

See [CHANGELOG.md](https://github.com/9orky/agentic/blob/main/CHANGELOG.md).

## Contributing

Ideas, issues, and pull requests are welcome.

Start with [CONTRIBUTING.md](https://github.com/9orky/agentic/blob/main/CONTRIBUTING.md).
