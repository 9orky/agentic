---
doc_class: policy
rule_kind: policy
scope: project
audience: agent
purpose: Tighten the shared feature rule with this repository's feature-root conventions.
applies_when:
  - The shared feature rule is already in scope.
  - The target is a feature package under this repository's feature layout.
tags:
  - project
  - feature
  - seam
read_directly: false
tightens_paths:
  - ../../../structure/feature/FEATURE.md
escalation_paths:
  - layers/INDEX.md
---

# Project Feature Module

## Required Decisions

- Name the feature-root seam other code may import.
- Name any feature-root entrypoint such as `cli.py`.
- Name the nested module folders that carry the feature's internal slices.

## Core Rules

- Keep the feature root small: package seam, explicit entrypoints, and nested module folders.
- Place most internal feature logic in nested module folders rather than directly at the feature root.
- Expose cross-feature access through the feature root or another explicit seam, not through deep imports.
- Do not treat the feature root as a dumping ground for mixed application, domain, or infrastructure files.

## Review Checks

- The feature root stays small.
- Entry points are explicit.
- Nested modules carry internal slices.
- Cross-feature access stays on explicit seams.