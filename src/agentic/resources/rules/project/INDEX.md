---
doc_class: navigational
rule_kind: navigation
scope: project
audience: agent
purpose: Route repository-local rule supplements after the matching shared branch is already known.
applies_when:
  - The shared rule branch is already in scope.
  - The task needs repository-local tightening rather than another shared branch.
tags:
  - project
  - routing
  - local
read_directly: false
tightens_paths:
  - ../INDEX.md
entrypoint: true
read_strategy: progressive
child_paths:
  - structure/INDEX.md
---

# Project Rules

## Use This Branch When

- The shared branch is already known.
- The task needs repository-local structure or naming rules.

## Stop Or Descend

- Read [structure/INDEX.md](structure/INDEX.md) when shared structure rules are in scope and the repository needs stricter local guidance.
- Stop here if the shared rules are already sufficient.

## Review Checks

- Shared guidance is already in scope before a local supplement is opened.
- The next local read is explicit.