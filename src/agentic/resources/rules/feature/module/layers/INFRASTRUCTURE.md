# Infrastructure Layer Rules

Document Class: navigational

## Purpose

Within the owning module, `infrastructure` routes concrete adapter work to the correct infrastructure rule set while keeping persistence, integrations, and shim design distinct from application and UI concerns.

## Use This When

1. Use this file when module ownership is already clear and the task belongs in `infrastructure`.
2. Use this file when the task affects persistence, boundary translation, external capability adapters, execution-environment integrations, or infrastructure shims.
3. Follow a child document when the task needs structure-specific or shim-specific rules.

## Available Options

| Document | Information You Can Obtain |
| --- | --- |
| [infrastructure/STRUCTURE.md](infrastructure/STRUCTURE.md) | the anchor and placement rules for repositories, concrete adapters, mappings, and inward-only dependencies |
| [infrastructure/SHIMS.md](infrastructure/SHIMS.md) | the rules for infrastructure layer shims and anchor shims, including when they should expose factory functions instead of concrete wiring internals |

## Navigation Rule

1. Stay in this file until it is clear whether the question is about infrastructure placement or infrastructure shim design.
2. Follow [infrastructure/STRUCTURE.md](infrastructure/STRUCTURE.md) when deciding where repository implementations, adapters, mappings, or translation logic belong.
3. Follow [infrastructure/SHIMS.md](infrastructure/SHIMS.md) when deciding what `infrastructure/__init__.py` or an anchor shim should export.
4. Keep workflow ownership in `application` even when infrastructure makes the concrete adapters available.
5. If the task is actually business modeling or delivery shaping, return to the owning module router and choose the correct sibling layer document.

## Local Context

`infrastructure` owns:

1. repository implementations
2. persistence mappings
3. external capability adapters and execution-environment integrations
4. representation mapping and boundary translation
5. concrete runtime adapters selected by the owning module's application flow

`infrastructure` may depend on `domain`, but not on `application` or `ui`.

Cross-layer consumers may import infrastructure symbols only through `infrastructure/__init__.py` or the owning anchor shim.

## Exit Condition

1. The next infrastructure rule is clear: [infrastructure/STRUCTURE.md](infrastructure/STRUCTURE.md), [infrastructure/SHIMS.md](infrastructure/SHIMS.md), or continued work inside the current file's local context.
2. The task still fits `infrastructure` rather than `application`, `domain`, or `ui`.