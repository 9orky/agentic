---
doc_class: policy
rule_kind: policy
scope: project
audience: agent
purpose: Define repository-local file-tree expectations for layered feature modules.
applies_when:
  - The shared layered file-tree rule is already in scope.
  - The target module follows this repository's canonical layered package layout.
tags:
  - project
  - file-tree
  - layers
read_directly: false
tightens_paths:
  - ../../../../structure/feature/layers/FILE_TREE.md
escalation_paths:
  - LAYERS.md
---

# Project Layer File Tree

## Required Decisions

- Name the package root for the current module.
- Name which canonical layer folders are present.
- Name any root seam files such as `__init__.py` or `cli.py`.
- Name the minimum starter files inside each present layer.

## Core Rules

- Keep the module root as a small package seam with `__init__.py` and only the root files that expose real seams.
- Use canonical layer folder names only: `application`, `domain`, `infrastructure`, and `ui`.
- Treat missing layer folders as normal when the module does not need those responsibilities.
- Keep optional root entrypoints such as `cli.py` at the module or feature root, not buried inside a layer folder.
- Grow the tree by adding files inside an owning canonical layer before inventing a new top-level branch.
- Start `domain/` with `entity.py` and `value_object.py`, then add `service.py` and `repository.py` only when the domain responsibilities require them.
- Start `application/` with `queries.py` and `commands.py` as thin orchestration files.
- When `application/queries.py` or `application/commands.py` becomes too large, replace that file with a folder where each query or command has its own file and keeps local DTOs when needed.
- Start `infrastructure/` with `__init__.py` plus concrete detail-oriented adapter files such as `file_repository.py`.
- Keep the default infrastructure export as a simple variable in `infrastructure/__init__.py` rather than a wide factory surface.

## Review Checks

- The module root stays small.
- Layer folders use canonical names only.
- Optional layers are omitted intentionally.
- New branches are justified by ownership rather than convenience.
- Starter files match the minimum scaffold for each present layer.