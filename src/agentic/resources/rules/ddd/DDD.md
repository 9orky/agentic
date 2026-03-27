# Domain-Driven Design Rules

Document Class: navigational

## Purpose

Use this file to route strategic and tactical domain-modeling work.

## Use This When

1. Use this file when the task changes business language, subdomains, bounded contexts, or context relationships.
2. Use this file when the task needs explicit tactical DDD classifications such as entity, value object, aggregate, repository, domain service, factory, policy, or domain event.
3. Use this file when planning must define or update a project-local `DDD.md` artifact.

## Available Options

| Document | Information You Can Obtain |
| --- | --- |
| [STRATEGIC.md](STRATEGIC.md) | the contract for the project-local `DDD.md` artifact that holds ubiquitous language, subdomains, bounded contexts, context map, and strategic boundary rules |
| [TACTICAL.md](TACTICAL.md) | the tactical classification rules for entities, value objects, aggregates, repositories, services, factories, policies, events, and code-facing ownership |

## Navigation Rule

1. Start with [STRATEGIC.md](STRATEGIC.md) when the work changes business language, strategic boundaries, or context relationships.
2. Read [TACTICAL.md](TACTICAL.md) when the work needs code-facing domain classifications, aggregate boundaries, or repository ownership decisions.
3. Return to [STRATEGIC.md](STRATEGIC.md) if tactical modeling reveals a hidden context split, translation boundary, or language conflict.
4. Keep the project-local `DDD.md` artifact aligned with the accepted strategic model before locking executable step files.

## Local Context

When a project-local strategic artifact is required, place `DDD.md` at the same directory level as the owning `PLAN.md`.

When a bounded context has a stable implementation root, keep its `TACTICAL.md` artifact near that root and make the tactical artifact reuse the same bounded-context name defined in the strategic model.

## Exit Condition

1. The next DDD document is clear.
2. If strategic modeling applies, the location and role of the project-local `DDD.md` artifact are explicit.