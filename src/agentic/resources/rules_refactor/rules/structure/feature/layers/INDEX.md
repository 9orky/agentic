---
doc_class: navigational
rule_kind: navigation
audience: agent
purpose: Route layered-module rules when layering is part of the structural contract.
applies_when:
  - The feature module uses explicit layers to constrain placement and dependency flow.
  - File-tree growth depends on the chosen layer model.
tags:
  - structure
  - layers
  - routing
entrypoint: true
read_strategy: progressive
read_directly: false
child_paths:
  - LAYERS.md
  - FILE_TREE.md
---

# Layers

## Use This Branch When

- Layer names and dependency direction are part of the design contract.
- The file tree should grow from the selected layer model.

## Stop Or Descend

- Read [LAYERS.md](LAYERS.md) to define allowed layers and dependency direction.
- Read [FILE_TREE.md](FILE_TREE.md) only when the layer model implies deterministic tree growth.
- Stop here if layers are incidental rather than contractual.

## Review Checks

- Layering is justified by design constraints, not style preference.
- File-tree rules are not applied before layer rules are clear.
