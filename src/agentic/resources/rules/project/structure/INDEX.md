---
doc_class: navigational
rule_kind: navigation
scope: project
audience: agent
purpose: Route repository-local structure supplements for this workspace.
applies_when:
  - Shared structure classification is already known.
  - The task needs local package, feature, layer, or tree conventions.
tags:
  - project
  - structure
  - routing
read_directly: false
tightens_paths:
  - ../../structure/INDEX.md
entrypoint: true
read_strategy: progressive
child_paths:
  - MODULE.md
  - feature/INDEX.md
---

# Project Structure

## Use This Branch When

- Shared module or feature structure is already in scope.
- The repository needs stricter local structure guidance.

## Stop Or Descend

- Read [MODULE.md](MODULE.md) for local package and public-seam rules.
- Descend to [feature/INDEX.md](feature/INDEX.md) when the target is already classified as a feature module.
- Stop here if the shared structure rules already explain the case.

## Review Checks

- Local structure guidance tightens the shared branch instead of replacing it.
- The agent stops at the shallowest local supplement that fits.