---
doc_class: navigational
rule_kind: navigation
scope: project
audience: agent
purpose: Route repository-local layer naming and file-tree supplements.
applies_when:
  - The shared layered-feature rule is already in scope.
  - The task needs this repository's canonical layer names or tree shape.
tags:
  - project
  - layers
  - routing
read_directly: false
tightens_paths:
  - ../../../../structure/feature/layers/INDEX.md
entrypoint: true
read_strategy: progressive
child_paths:
  - LAYERS.md
  - FILE_TREE.md
---

# Project Layer Structure

## Use This Branch When

- Shared layered-module rules are already in scope.
- The repository needs concrete layer names or file-tree constraints.

## Stop Or Descend

- Read [LAYERS.md](LAYERS.md) for the canonical layer names and dependency meaning.
- Read [FILE_TREE.md](FILE_TREE.md) when the local file tree must follow the local layered structure.
- Stop here if no local layer specialization is needed.

## Review Checks

- Local layer names are taken from project rules, not guessed from code.
- File-tree specialization is opened only after layer naming is known.