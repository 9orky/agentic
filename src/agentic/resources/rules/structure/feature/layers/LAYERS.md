---
doc_class: policy
rule_kind: policy
audience: agent
purpose: Define allowed layers and dependency direction inside a layered module.
applies_when:
  - The module has explicit layers that constrain placement.
  - Dependency direction must be enforced inside the module.
tags:
  - structure
  - layers
  - dependencies
read_directly: false
escalation_paths:
  - ../../../../project/structure/feature/layers/LAYERS.md
  - FILE_TREE.md
  - ../../../architecture/DEPENDENCIES.md
  - ../../../architecture/OWNERSHIP.md
---

# Layered Module

## Required Decisions

- Name the allowed layers.
- Name the dependency direction between layers.
- Name the owning layer for each touched responsibility.

## Core Rules

- Use only layers that impose meaningful placement and dependency constraints.
- Each responsibility belongs to one owning layer.
- Dependency direction is explicit and one-way.
- Reject cross-layer shortcuts that bypass the chosen seam.

## Review Checks

- The allowed layers are explicit.
- Dependency direction is explicit.
- Cross-layer shortcuts are rejected.
- The layer model constrains real decisions.
