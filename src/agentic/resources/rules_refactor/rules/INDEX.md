---
doc_class: navigational
rule_kind: navigation
audience: agent
purpose: Route rule lookup to the shallowest branch that fits the current task.
applies_when:
  - Starting rule selection for a task or target folder.
tags:
  - routing
  - rules
entrypoint: true
read_strategy: progressive
read_directly: true
child_paths:
  - structure/INDEX.md
  - project/INDEX.md
  - architecture/INDEX.md
  - change/INDEX.md
  - execution/INDEX.md
  - verification/INDEX.md
---

# Rules

## Stop Or Descend

- Stop here if the task does not need branch-specific rules yet.
- Descend only to the first branch whose assumptions fit the current task.
- Prefer the shallowest matching branch over deeper specialization.
- For code-shape questions, classify structure before applying architecture, change, or verification rules.
- Enter [project/INDEX.md](project/INDEX.md) only after the matching shared branch is already known and repository-local tightening is needed.

## Branches

- [structure/INDEX.md](structure/INDEX.md): classify a target as a module, feature module, or layered specialization
- [project/INDEX.md](project/INDEX.md): apply repository-local supplements after the shared branch is already in scope
- [architecture/INDEX.md](architecture/INDEX.md): ownership, boundary, and dependency rules for structural placement
- [change/INDEX.md](change/INDEX.md): rules for reshaping or replacing existing implementation
- [execution/INDEX.md](execution/INDEX.md): execution artifacts used before and during implementation
- [verification/INDEX.md](verification/INDEX.md): testing and proof rules for validating behavior

## Review Checks

- The next read is explicit.
- No deeper branch is opened without a matching need.
- Structure is classified before deeper structural constraints are applied.
- Project-local rules are not opened before the shared branch is known.