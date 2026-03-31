---
doc_class: policy
rule_kind: policy
audience: agent
purpose: Define deterministic file-tree growth for a layered module.
applies_when:
  - The layered module has a required or strongly preferred file-tree pattern.
  - New files should be placed according to layer-owned growth rules.
tags:
  - structure
  - file-tree
  - layers
read_directly: false
escalation_paths:
  - ../../../../project/structure/feature/layers/FILE_TREE.md
  - LAYERS.md
  - ../../../architecture/BOUNDARIES.md
  - ../../../change/REFACTORING.md
---

# Layer File Tree

## Required Decisions

- Name the required top-level folders or files for the module.
- Name the owning layer for each new file.
- Name the stable public seams the tree must preserve.

## Core Rules

- The file tree grows from the chosen layer model rather than from convenience.
- Add a file in the owning layer first, not in the nearest existing folder.
- Keep public seams stable while internal structure grows inward.
- Do not invent new tree branches unless the current layer rules require them.

## Review Checks

- Tree growth follows layer ownership.
- Public seams remain minimal.
- New files are not placed by convenience alone.
- The tree reflects responsibility and dependency rules.
