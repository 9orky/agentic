# Feature Rules

A feature owns one business capability and one public boundary.

This file is the bootstrap document for feature-shape questions.

Read one child document only when the task needs that layer's detail.

## Feature Rule Options

| Document | Information You Can Obtain |
| --- | --- |
| [layers/DOMAIN.md](layers/DOMAIN.md) | domain ownership rules for entities, value objects, domain services, invariants, and domain-owned repository contracts |
| [layers/INFRASTRUCTURE.md](layers/INFRASTRUCTURE.md) | infrastructure ownership rules for persistence, external systems, runtime integrations, and concrete adapters |
| [layers/APPLICATION.md](layers/APPLICATION.md) | application ownership rules for use cases, orchestration, application services, and feature-to-feature coordination |
| [layers/UI.md](layers/UI.md) | UI ownership rules for command binding, delivery entrypoints, presenters, request parsing, and response shaping |

## Shared Default Shape

Under the shared default, a feature is organized through these layers:

1. `domain`
2. `infrastructure`
3. `application`
4. `ui`

Use the layer file that provides the ownership detail you need instead of inferring it here.