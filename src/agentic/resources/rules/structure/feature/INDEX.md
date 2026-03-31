---
doc_class: navigational
rule_kind: navigation
audience: agent
purpose: Route stricter rules when the module is a feature-shaped unit.
applies_when:
  - The target module owns a user-visible or business capability.
  - The base module rule is not strict enough to explain the boundary.
tags:
  - structure
  - feature
  - routing
entrypoint: true
read_strategy: progressive
read_directly: false
child_paths:
  - FEATURE.md
  - layers/INDEX.md
---

# Feature Structure

## Use This Branch When

- The target is a module first, but it also owns a feature boundary.
- Capability ownership and cross-feature access rules need stricter control.

## Stop Or Descend

- Read [FEATURE.md](FEATURE.md) for the feature-module rule.
- Descend to [layers/INDEX.md](layers/INDEX.md) only when layers are part of the contract.
- Stop here if the module is not feature-shaped.

## Review Checks

- Feature is treated as a stricter module, not a different base abstraction.
- Layer rules are not opened unless layering is intentional.
