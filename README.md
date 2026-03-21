# agentic

`agentic` is a pipx-first CLI that bootstraps a project-local `agentic/` folder and uses that folder as the durable rule and architecture contract for a project.

The installed package gives you the command.

The generated local `agentic/` folder gives your project a stable, repo-specific rule set and architecture contract.

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

It is safe to rerun. Existing local files are preserved instead of overwritten.

After bootstrap, review `agentic/agentic.yaml`, adjust boundaries or exclusions as needed, and run:

```bash
agentic check
```

## Deterministic Usage Checklist

Use this checklist from first bootstrap through steady-state use:

1. Bootstrap the local collaboration surface with `agentic` if `agentic/` does not exist yet or is missing expected shared files.
2. Review the generated rules and config before changing code against them.
3. If rules or architecture are still underspecified, run a first-configuration interview with the user before making boundary or ownership decisions.
4. Record durable decisions only in the local contract:
  - `agentic/agentic.yaml` for config, exclusions, and boundaries
  - `agentic/rules/overrides/` for repo-local replacements of shared rules
  - `agentic/rules/project-specific/` for new repo-local rules
5. After meaningful rule, config, or code changes, rerun `agentic check`.
6. Use `agentic update` only to refresh packaged shared docs, then rerun `agentic check`.
7. Keep `agentic/` readable for future sessions: no scratchpads, temporary logs, or disposable notes.

## Communication Model

The local `agentic/` folder is the shared contract for architecture rules and workspace conventions.

In practice that means:

1. bundled core docs under `agentic/rules/*.md` define stable rails,
2. `agentic/rules/overrides/` records repo-local updates to those core docs,
3. `agentic/rules/project-specific/` records new repo-local rules future runs must inherit,
4. `agentic/agentic.yaml` records the user-editable architecture agreement,
5. language-specific extractors build one common architecture map shape so checks operate on the same structure.

`agentic/` is not a scratchpad. It is the durable surface that future sessions should be able to read without hidden context.

## Generated Project Structure

After running `agentic` in a project, the local structure looks like this:

```text
my-project/
├── agentic/
│   ├── agentic.yaml
│   └── rules/
│       ├── AGENT.md
│       ├── FEATURE.md
│       ├── MODULE.md
│       ├── PLANNING.md
│       ├── REFACTORING.md
│       ├── TESTS.md
│       ├── overrides/
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

Rule evaluation does not read source files directly in the checker. Each language extractor emits one shared architecture-map shape keyed by repo-relative file path. Each entry contains `imports`, `classes`, and `functions`, and the checker evaluates boundaries against that normalized data.

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

Use `agentic help` or `agentic --help` to discover the command surface in a target project.

The stable top-level workflow is:

1. `agentic` bootstraps or refreshes the local collaboration surface safely.
2. `agentic check` validates the configured architecture boundaries.
3. `agentic update` refreshes packaged shared rules.

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

## Working Contract

The generated `agentic/` folder is meant to become a long-lived architecture boundary for a project.

The expected operating model is:

1. shared core docs under `agentic/rules/*.md` stay stable and may be refreshed by `agentic update`,
2. local updates to those core docs go under `agentic/rules/overrides/`,
3. new repo-specific rules go under `agentic/rules/project-specific/`,
4. the architecture config in `agentic/agentic.yaml` defines technical boundaries,
5. first configuration is an interactive conversation with the user about boundaries, exclusions, ownership, and update habits,
6. `agentic check` is the architecture validation boundary and `agentic update` is the shared-rule refresh boundary.

Operationally, the safest default is:

1. `agentic` ensures the local collaboration surface exists.
2. the user closes missing decisions through a first-configuration interview.
3. durable decisions are written back into `agentic/`.
4. `agentic check` validates the result.

When a repo-specific clarification is needed, record it in the smallest applicable extension folder.

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
2. `src/agentic/features/architecture_check/`
