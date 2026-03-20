# agentic

`agentic` is a pipx-first CLI that bootstraps a project-local `agentic/` folder and uses that folder as the durable communication boundary between a user and the user's LLM.

The installed package gives you the command.

The generated local `agentic/` folder gives your project a stable, repo-specific rule set, architecture contract, and handoff surface that humans and LLMs can share.

## Install

End users should install it with `pipx`:

```bash
pipx install agentic
```

During local development of this repository, refresh your localhost install with one command:

```bash
make dev-refresh
```

That runs:

```bash
pipx install --force --editable .
```

## User Workflow

In any project root:

```bash
agentic
```

If the current directory does not already contain an `agentic/` folder, the command creates it and copies:

1. the bundled shared rules shipped with the package
2. a starter YAML config file at `agentic/agentic.yaml`

It does not overwrite existing local files.

After bootstrap, the command prints the next step:

```bash
agentic --llm
```

That command prints the handoff prompt for the user's LLM. The intent is:

1. the LLM reads the shared `agentic` rules,
2. reads the extracted architecture-map contract,
3. scans the repository,
4. asks the user to define missing architecture boundaries,
5. writes project-specific guidance into `agentic/rules/project-specific/`,
6. and establishes the local `agentic/` folder as the project's SSOT.

## Communication Model

The local `agentic/` folder is the shared contract between the user and the user's LLM.

In practice that means:

1. bundled docs under `agentic/rules/` define stable rails,
2. `agentic/guide/` contains operational usage docs,
3. `agentic/reference/` contains technical reference docs,
4. `agentic/agentic.yaml` records the user-editable architecture agreement,
5. `agentic/rules/project-specific/` records repo-specific clarifications future LLM runs must inherit,
6. language-specific extractors build one common architecture map shape so checks and LLM reasoning operate on the same structure.

`agentic/` is not a scratchpad. It is the durable surface that future sessions should be able to read without hidden context.

## Generated Project Structure

After running `agentic` in a project, the local structure looks like this:

```text
my-project/
├── agentic/
│   ├── agentic.yaml
│   ├── guide/
│   │   ├── COMMANDS.md
│   │   └── WORKFLOW.md
│   ├── reference/
│   │   └── ARCHITECTURE_MAP.md
│   └── rules/
│       ├── AGENT.md
│       ├── FEATURE.md
│       ├── MODULE.md
│       ├── PLAN_STEP_TEMPLATE.md
│       ├── PLANNING.md
│       ├── REFACTORING.md
│       ├── TESTS.md
│       └── project-specific/
└── src/
```

Treat that generated `agentic/` directory as the project's working rule set.

The installed Python package is only the delivery mechanism.

The runtime extracts project facts through per-language scripts, normalizes them into one architecture-map shape, and evaluates rules against that shared structure.

## Configuration

The canonical config format is YAML:

```yaml
language: python

exclusions:
  - tests/**
  - node_modules/**
  - dist/**
  - build/**
  - .venv/**
  - agentic/**

rules:
  boundaries:
    - source: src/domain
      disallow:
        - src/infra
        - src/ui

    - source: src/features/*
      disallow:
        - src/features/*
      allow_same_match: true
      allow:
        - src/features/*
```

Config is validated with Pydantic when `agentic check` runs.

Rule evaluation does not read source files directly in the checker. Each language extractor emits one shared architecture-map shape, documented in `agentic/reference/ARCHITECTURE_MAP.md`, and the checker evaluates boundaries against that normalized data.

Boundary rules support glob patterns.

Practical behavior:

1. `source` is scope-aware, so `src/features/*` matches files under any feature subtree.
2. `disallow` is also scope-aware, so `src/features/*` blocks imports into sibling feature internals.
3. `allow` is exact-glob matching, which lets you permit stable public entrypoints such as a feature root import without allowing every nested internal file.
4. `allow_same_match: true` lets the same wildcard capture import itself, so new features can be added without revisiting config.

That means a feature rule can be configured once and stay stable as new sibling features appear.

Supported config locations, in order:

1. `--config <path>`
2. `agentic/agentic.yaml`
3. `agentic/agentic.yml`
4. `agentic.yaml`
5. `agentic.yml`

## Commands

The bootstrapped `agentic/guide/COMMANDS.md` file is the short command reference intended for future human and LLM runs.

Bootstrap the local folder:

```bash
agentic
```

Explicit bootstrap:

```bash
agentic init
```

Refresh shared docs in an existing project:

```bash
agentic update
agentic update --project-root /path/to/project
```

Print the LLM handoff prompt:

```bash
agentic --llm
```

Print the command summary:

```bash
agentic help
agentic --help
```

Run the architecture checker:

```bash
agentic check
```

Run against another project root or config:

```bash
agentic check --project-root /path/to/project
agentic check --config /path/to/agentic.yaml
```

## Language Support

Current architecture extraction support:

1. Python
2. TypeScript and JavaScript via `node`
3. PHP via `php`

If you run TypeScript or PHP checks, the corresponding runtime must be available on `PATH`.

## LLM Contract

The generated `agentic/` folder is meant to become a long-lived collaboration boundary for LLM work.

The expected operating model is:

1. shared docs under `agentic/rules/` stay stable,
2. `agentic/guide/` documents how to operate the local contract during a session,
3. `agentic/reference/ARCHITECTURE_MAP.md` explains the shared extracted schema the checker and LLMs rely on,
4. project-specific rules are added under `agentic/rules/project-specific/`,
5. the architecture config in `agentic/agentic.yaml` defines technical boundaries,
6. future LLM runs read the guide docs first and then use `agentic/rules/AGENT.md` for coding rules.

When a repo-specific clarification is needed, record it in `project-specific/`.

When a shared bundled rule is wrong or incomplete, keep the local clarification explicit and note that the package itself should be improved upstream rather than silently mutating the shared rail for one repo.

## Development

Run the test suite with:

```bash
make test
```

## Package Layout

The canonical implementation lives in `src/agentic/`.

Its feature boundaries are:

1. `src/agentic/features/workspace_contract/`
2. `src/agentic/features/configuration/`
3. `src/agentic/features/architecture_check/`
4. `src/agentic/features/llm_handoff/`
