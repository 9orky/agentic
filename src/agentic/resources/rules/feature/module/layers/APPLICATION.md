# Application Layer Rules

Document Class: navigational

## Purpose

Within the owning module, `application` routes use-case work to the correct application seam and keeps orchestration distinct from domain, infrastructure, and UI concerns.

## Use This When

1. Use this file when module ownership is already clear and the task belongs in `application`.
2. Use this file when the task affects commands, queries, workflow orchestration, transaction boundaries, or feature-to-feature adaptation.
3. Follow a child document when the task needs command-specific or query-specific rules.

## Available Options

| Document | Information You Can Obtain |
| --- | --- |
| [application/COMMANDS.md](application/COMMANDS.md) | the write-side command rules for naming, state change, port-agnostic invocation, and command-local DTO placement |
| [application/QUERIES.md](application/QUERIES.md) | the read-side query rules for naming, returned DTOs, port-agnostic invocation, and no-rendering data contracts |

## Navigation Rule

1. Stay in this file until it is clear whether the use case is a command, a query, reusable application orchestration, or feature-to-feature adaptation.
2. Follow [application/COMMANDS.md](application/COMMANDS.md) when the use case changes system state.
3. Follow [application/QUERIES.md](application/QUERIES.md) when the use case reads data without changing system state.
4. Keep reusable orchestration behind `services` and feature-to-feature adaptation behind `adapters` rather than creating extra root anchors.
5. If the work is actually business modeling, concrete integration, or delivery parsing or rendering, return to the owning module router and choose the correct sibling layer document.

## Local Context

Under the shared default, `application/` is organized only behind these anchors:

1. `commands`
2. `queries`
3. `services` when reusable orchestration is needed
4. `adapters` when feature-to-feature adaptation is needed

Commands and queries are the primary use-case seams.

`services` and `adapters` are internal application implementation anchors unless an explicit anchor shim is intentionally exposed.

`application` may depend on `domain` and `infrastructure`, but not on `ui`.

Cross-layer consumers may import application symbols only through `application/__init__.py` or an explicitly approved application anchor shim.

## Exit Condition

1. The next application rule is clear: [application/COMMANDS.md](application/COMMANDS.md), [application/QUERIES.md](application/QUERIES.md), or continued work inside the current file's local context for `services` or `adapters` placement.
2. The task still fits `application` rather than `domain`, `infrastructure`, or `ui`.