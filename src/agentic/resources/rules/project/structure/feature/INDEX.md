---
doc_class: navigational
rule_kind: navigation
scope: project
audience: agent
purpose: Route repository-local feature supplements after shared feature classification is known.
applies_when:
  - The target is already classified as a feature module.
  - The repository needs stricter local feature or layer guidance.
tags:
  - project
  - feature
  - routing
read_directly: false
tightens_paths:
  - ../../../structure/feature/INDEX.md
entrypoint: true
read_strategy: progressive
child_paths:
  - FEATURE.md
  - layers/INDEX.md
---

# Project Feature Structure

## Use This Branch When

- Shared feature rules are already in scope.
- The repository needs stricter feature-root or layered-feature guidance.

## Stop Or Descend

- Read [FEATURE.md](FEATURE.md) for local feature-root constraints.
- Descend to [layers/INDEX.md](layers/INDEX.md) when the feature module is layered.
- Stop here if the shared feature rule already fits.

## Review Checks

- Local feature rules supplement the shared feature rule.
- Layer supplements are opened only for layered feature modules.