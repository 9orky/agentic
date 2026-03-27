# Application Query Rules

Document Class: leaf

## Purpose

Within the owning module's `application` layer, queries own read-side use cases that return data without changing system state.

## Applies When

Read this file when the use case retrieves or describes data for the owning module and must remain read-only.

## Ownership

Query files own:

1. one self-descriptive read-side use case
2. the query-specific input DTOs required to request the data, when any exist
3. the returned DTOs that define the query result
4. read-side orchestration of domain and infrastructure collaborators needed to assemble the result

Queries are called from `ui` and may be invoked through many delivery ports, so the query contract must stay port-agnostic.

## Core Rules

### Naming

1. Name each query by the data it retrieves or describes.
2. The query name must be self-descriptive without relying on the caller's delivery context.
3. If the name describes a mutation, lifecycle transition, or side effect, it is not a query.

### Read Contract

1. A query returns DTOs.
2. A query does not change system state.
3. A query returns data only and must not perform rendering or presentation shaping.

### DTO Placement

1. Keep DTOs that belong only to one query in that query file or inside that query's package when package form is used.
2. Do not create a generic DTO bucket at the `application/` root.
3. Extract a shared DTO only when more than one application seam uses the same returned or input contract intentionally.

## Constraints

1. Do not put rendering, presentation shaping, or delivery parsing in a query.
2. Do not hide state changes inside a query.
3. Do not return delivery-specific response models from a query.
4. Do not move business classification into a query just to simplify data assembly.

## Acceptance Check

1. The query name is self-descriptive about the data it retrieves.
2. The query returns DTOs and stays read-only.
3. The query contract stays usable from multiple delivery ports.
4. Query-specific DTOs stay with the query instead of leaking into generic application buckets.