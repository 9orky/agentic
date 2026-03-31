---
doc_class: policy
rule_kind: policy
scope: project
audience: agent
purpose: Define the canonical layer names and dependency meaning used by layered feature modules in this repository.
applies_when:
  - The shared layered-feature rule is already in scope.
  - The target module follows this repository's layered feature convention.
tags:
  - project
  - layers
  - dependencies
read_directly: false
tightens_paths:
  - ../../../../structure/feature/layers/LAYERS.md
escalation_paths:
  - FILE_TREE.md
  - ../../../../architecture/DEPENDENCIES.md
---

# Project Layered Module

## Required Decisions

- Choose which of the canonical layers the module actually needs.
- Name the owning layer for each touched responsibility.
- Name the allowed cross-layer seams for the current change.
- Name the minimum starter files each present layer must own.

## Core Rules

- Use only the canonical layer names `application`, `domain`, `infrastructure`, and `ui` for governed layered feature modules.
- A module may omit any canonical layer it does not need.
- `ui` depends inward through explicit seams and must not reach domain or infrastructure internals directly.
- `application` coordinates use cases and may depend on `domain` contracts and infrastructure seams.
- `domain` holds core business rules and stays free of delivery and infrastructure concerns.
- `infrastructure` implements outward-facing concerns and depends inward on stable contracts rather than the reverse.
- New layer names require a project-rule change before they are used in code.

## Layer Starter Rules

- `domain` starts with `entity.py` and `value_object.py`.
- Add `domain/service.py` when the module needs domain logic that should not live inside one entity or value object.
- Add `domain/repository.py` only when the domain needs an abstract IO seam for loading or persisting owned entities.
- `application` stays orchestration-only and uses domain services plus infrastructure seams to load entities and coordinate state changes.
- `application` starts with `queries.py` and `commands.py`.
- Keep application DTOs optional and local to the query or command file until growth justifies extraction.
- `infrastructure` uses detail-oriented adapter names such as `file_repository.py` when implementing a repository or other external seam.
- `infrastructure/__init__.py` exports a simple ready-to-use variable for each concrete adapter that should be consumed as a default seam.

## Review Checks

- Only canonical layer names are used.
- Missing layers are intentional.
- Dependency meaning for each present layer is explicit.
- No new layer name is introduced ad hoc.
- Each present layer starts from the minimum scaffold before deeper structure is added.