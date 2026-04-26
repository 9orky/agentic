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

- [src/agentic/features/workspace/](/Users/gorky/Projects/agentic/src/agentic/features/workspace) owns project bootstrap, update, code generation, and packaged rule-schema validation.
- `sync/` owns the generated contract layout and file mirroring behavior.
- `code/` owns packaged code-generation recipes.
- `rules/` owns schema checks for packaged markdown rule documents.

### Architecture

- [src/agentic/features/architecture/](/Users/gorky/Projects/agentic/src/agentic/features/architecture) owns dependency extraction, boundary analysis, and hotspot reporting.
- `map/` owns config loading, extractor orchestration, and dependency-graph construction.
- `check/` owns policy evaluation and reporting.
- `hotspots/` owns hotspot analysis over the same dependency graph.
- `summary/` owns agent-facing repository briefings built from the same graph.
- The feature is exposed through `agentic architecture check`, `agentic architecture hotspots`, and `agentic architecture summary`.

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

## Boundary

Refresh this page against the live repo structure before treating it as authoritative.
