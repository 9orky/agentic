# Feature Module Rules

Document Class: navigational

## Purpose

Within a feature, a module is the first structural owner below the feature boundary.

## Use This When

1. Use this file after [../FEATURE.md](../FEATURE.md) has established that the responsibility belongs inside the current feature.
2. Use this file when the task needs module-first ownership or module-layer placement guidance.
3. Read exactly one child layer document only after module ownership is already clear.

## Available Options

| Document | Information You Can Obtain |
| --- | --- |
| [../../module/MODULE.md](../../module/MODULE.md) | the generic module boundary contract for public seams, private internals, and dependency direction |
| [layers/DOMAIN.md](layers/DOMAIN.md) | domain ownership rules for entities, value objects, domain services, invariants, and domain-owned repository contracts inside the current module |
| [layers/INFRASTRUCTURE.md](layers/INFRASTRUCTURE.md) | the infrastructure bootstrap that routes to structure and shim rules for persistence, runtime integrations, and concrete adapters inside the current module |
| [layers/APPLICATION.md](layers/APPLICATION.md) | the application bootstrap that routes to command and query rules and keeps services or adapters behind the application layer inside the current module |
| [layers/UI.md](layers/UI.md) | UI ownership rules for command binding, delivery entrypoints, presenters, request parsing, and response shaping inside the current module |

## Navigation Rule

1. Confirm the responsibility belongs to one module inside the current feature.
2. Use [../../module/MODULE.md](../../module/MODULE.md) when the question is about module boundary shape, seams, or dependency rules.
3. Use exactly one linked layer document when the question is about placement inside the owning module.
4. Do not skip to a layer document before module ownership is clear.

## Local Context

Under the shared default, a module owns this layer set:

1. `domain`
2. `infrastructure`
3. `application`
4. `ui`

The module is the structural parent of that layer set.

## Exit Condition

1. The owning module is clear.
2. The next read is either [../../module/MODULE.md](../../module/MODULE.md) for module-shape questions or one linked module-layer document for placement questions.