---
doc_class: policy
rule_kind: policy
scope: project
audience: agent
purpose: Tighten the shared module rule with repository-local Python package and seam conventions.
applies_when:
  - The shared module rule is already in scope.
  - The target module is an importable Python package in this repository.
tags:
  - project
  - structure
  - module
  - python
read_directly: false
tightens_paths:
  - ../../structure/MODULE.md
escalation_paths:
  - feature/INDEX.md
---

# Project Module

## Required Decisions

- Name the package root that forms the module seam.
- Name the explicit public imports exposed from `__init__.py`, if any.
- Name any non-package entrypoint such as `cli.py` that belongs at the module root.

## Core Rules

- Treat an importable Python package root as the module seam for local structure decisions.
- Keep `__init__.py` minimal and export only the public names that real consumers need.
- Keep module-root entrypoints such as `cli.py` explicit instead of hiding bootstrap behavior in internal files.
- Do not expose nested layer folders or helper modules through convenience re-exports.

## Review Checks

- The package root is explicit.
- `__init__.py` stays minimal.
- Module-root entrypoints are explicit.
- Local package conventions do not widen the shared module API rule.