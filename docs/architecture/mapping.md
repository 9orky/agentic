# Architecture Mapping

This page is the maintained high-level map of the current `agentic` repository.

## Top-Level Structure

- [README.md](/Users/gorky/Projects/agentic/README.md): short landing page for the project
- [docs/](/Users/gorky/Projects/agentic/docs): human-facing project documentation
- [src/agentic/](/Users/gorky/Projects/agentic/src/agentic): packaged runtime code and packaged resources
- [agentic/](/Users/gorky/Projects/agentic/agentic): workspace-facing contract content kept in the repo for development and inspection
- [tests/](/Users/gorky/Projects/agentic/tests): tests for runtime behavior

## Runtime Areas

### CLI Surface

- [src/agentic/cli.py](/Users/gorky/Projects/agentic/src/agentic/cli.py) registers the top-level `agentic` command group.
- The default command path invokes `init` when no subcommand is provided.

### Workspace Contract

- [src/agentic/features/workspace_contract/](/Users/gorky/Projects/agentic/src/agentic/features/workspace_contract) owns project bootstrap, update, and packaged rule-schema validation.
- `sync/` owns the generated contract layout and file mirroring behavior.
- `rules/` owns schema checks for packaged markdown rule documents.

### Architecture Check

- [src/agentic/features/architecture_check/](/Users/gorky/Projects/agentic/src/agentic/features/architecture_check) owns dependency extraction, boundary analysis, and hotspot reporting.
- The feature is exposed through `agentic check` and `agentic hotspots`.

## Packaged Versus Generated Assets

### Packaged Assets

- [src/agentic/resources/](/Users/gorky/Projects/agentic/src/agentic/resources) contains runtime data that ships with the package.
- [src/agentic/resources/rules/](/Users/gorky/Projects/agentic/src/agentic/resources/rules) is the packaged shared rule corpus.

### Generated Or Workspace-Owned Assets

- [agentic/agentic.yaml](/Users/gorky/Projects/agentic/agentic/agentic.yaml) is the workspace-facing architecture config in this repository snapshot.
- [agentic/rules/](/Users/gorky/Projects/agentic/agentic/rules) is the workspace-facing rule contract surface.
- [agentic/rules/local/](/Users/gorky/Projects/agentic/agentic/rules/local) is the only repo-local profile surface inside that contract.

## Documentation Split

- `docs/` explains the project to humans.
- `agentic/` is the live project contract that agents and humans inspect while operating on a repository.
- `src/agentic/resources/rules/` defines packaged rule assets for the runtime.
- The two surfaces should stay conceptually separate.

## Drift Note

The legacy page [docs/architecture-mapping.md](/Users/gorky/Projects/agentic/docs/architecture-mapping.md) drifted into an architecture-check config guide rather than a repository architecture map. Its useful feature-guide content belongs in [../runtime/architecture-check.md](/Users/gorky/Projects/agentic/docs/runtime/architecture-check.md), while this page becomes the maintained architecture map.

## Source Inputs

- [docs/architecture-mapping.md](/Users/gorky/Projects/agentic/docs/architecture-mapping.md)
- Current repository structure and code layout

## Boundary

Refresh this page against the live repo structure before treating it as authoritative. The legacy source page may drift.