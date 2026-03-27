# Application Command Rules

Document Class: leaf

## Purpose

Within the owning module's `application` layer, commands own write-side use cases that change system state.

## Applies When

Read this file when the use case creates, updates, deletes, or otherwise commits a state change through the owning module.

## Ownership

Command files own:

1. one self-descriptive write-side use case
2. the command-specific input DTOs required to run that use case, when any exist
3. command-local result DTOs only when the write-side contract needs explicit returned data
4. orchestration of domain and infrastructure collaborators needed to complete the state change

Commands are called from `ui` and may be invoked through many delivery ports, so the command contract must stay port-agnostic.

## Core Rules

### Naming

1. Name each command by the state-changing effect it performs.
2. The command name must be self-descriptive without relying on the caller's delivery context.
3. If the name describes only lookup, formatting, or reporting, it is not a command.

### State Change Contract

1. A command changes system state by creating, updating, deleting, or otherwise committing managed resources.
2. If the use case does not change state, model it as a query instead.
3. Keep the write-side workflow in the command and reusable orchestration in application services when multiple commands or queries need it.

### DTO Placement

1. Keep DTOs that belong only to one command in that command file or inside that command's package when package form is used.
2. Do not create a generic DTO bucket at the `application/` root.
3. Extract a shared DTO only when more than one application seam uses the same contract intentionally.

## Constraints

1. Do not put rendering, presentation shaping, or delivery parsing in a command.
2. Do not let a command name hide a read-only use case.
3. Do not move business invariants out of `domain` just because the command coordinates them.
4. Do not let command code depend on one delivery port's request or response model.

## Acceptance Check

1. The command name is self-descriptive about the state change it performs.
2. The use case changes system state and is not a disguised query.
3. The command contract stays usable from multiple delivery ports.
4. Command-specific DTOs stay with the command instead of leaking into generic application buckets.