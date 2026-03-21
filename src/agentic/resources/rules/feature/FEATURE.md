# Feature Rules

Document Class: navigational

## Purpose

A feature owns one business capability and one public boundary.

## Use This When

1. Use this file when the task needs feature-shape or layer-ownership guidance.
2. Read exactly one child document only when the task needs that layer's detail.

## Available Options

| Document | Information You Can Obtain |
| --- | --- |
| [layers/DOMAIN.md](layers/DOMAIN.md) | domain ownership rules for entities, value objects, domain services, invariants, and domain-owned repository contracts |
| [layers/INFRASTRUCTURE.md](layers/INFRASTRUCTURE.md) | infrastructure ownership rules for persistence, external systems, runtime integrations, and concrete adapters |
| [layers/APPLICATION.md](layers/APPLICATION.md) | application ownership rules for use cases, orchestration, application services, and feature-to-feature coordination |
| [layers/UI.md](layers/UI.md) | UI ownership rules for command binding, delivery entrypoints, presenters, request parsing, and response shaping |

## Navigation Rule

1. Stay in this document until the needed owning layer is clear.
2. Follow only the layer link that resolves the current ownership question.
3. Do not infer layer placement here when a linked layer file can decide it directly.

## Local Context

Under the shared default, a feature is organized through these layers:

1. `domain`
2. `infrastructure`
3. `application`
4. `ui`

## Exit Condition

1. You have identified the owning layer for the responsibility in question.
2. The next read is the single linked layer document that resolves that ownership.