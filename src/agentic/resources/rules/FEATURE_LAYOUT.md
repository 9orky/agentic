# Feature Layout Constraints

Layout constraints trees will include following labels:

- (REQ) always present, even empty
- (EXT) required when complexity grows
- (FUN) required when functionallity requires it

## Meaning Of Minimum Layout

Minimum layout means baseline anchors, not a ceiling on internal structure.

1. A minimum layout names the required structural anchors a layer must expose under the shared default.
2. It does not forbid additional files or subfolders inside the same owning layer when complexity requires modularity.
3. Added modularity must preserve the same owner, dependency direction, and public seam discipline.
4. Do not add extra peer architectural buckets to get that modularity. Grow inside the owning layer instead.
5. When an anchor grows too large, it may be implemented as multiple internal modules or subfolders with the same owning concept.
6. Use the simplest valid form first, then split only when private composition, scale, or change isolation requires it.
7. If another governing rule would be violated by the simple file form, prefer the package form of the same anchor rather than weakening the rule.

## Anchor Form Rule

When a layer layout names an anchor, that anchor may be implemented either as a file or as a same-named package unless the layer-specific rules narrow it further.

1. Keep the anchor name stable whether the implementation uses file form or package form.
2. Use file form when the anchor is still one coherent implementation slice.
3. Use package form when the anchor needs multiple private modules, multiple owned classes, multiple delivery handlers, or internal composition that would otherwise spill into loose sibling files.
4. In package form, `__init__.py` is only the export seam for that anchor unless the layer-specific rules say otherwise.
5. Do not split one anchor across both a peer file and a peer package with different names.
6. Do not create loose helper files beside a named anchor when those helpers still belong to that anchor. Move them behind the anchor package instead.

## Layer Shim Rule

Layer crossings must use shims, not deep imports.

1. Every layer exposes the minimum symbols needed by other layers through a shim.
2. The default shim is the layer `__init__.py`, or an owning anchor `__init__.py` when the layer is modularized by anchors.
3. A different layer may import only from that shim, never from an internal file behind it.
4. If a crossing import needs a new symbol, update the target shim instead of deep-importing the internal implementation file.
5. This rule applies only to cross-layer imports. Imports inside the same layer may use internal modules directly.

## Feature Iron Rule

Feature implementation is class-based across all layers under the shared default.

1. In feature code, model behavior through classes, methods, and class relationships.
2. Free functions are forbidden in feature layers under the shared default.
3. One class per file is mandatory across feature layers under the shared default.
4. If a layer anchor would otherwise need multiple classes in one file, use package form and keep one class per file behind the anchor shim.
5. Module-level constants are allowed only when they support a class and do not become a parallel procedural API.
6. Helper logic that cannot justify a class likely belongs in another owning type, another layer, or needs a tighter model.

## Domain

- default layer
- always present

### Ownership

- business rules and core domain concepts
- entities, value objects, policies, invariants, and pure transforms
- business-owned abstractions
- no dependencies on other layers or packages

### Domain Iron Rule

Domain is the strictest expression of the feature-wide class rule.

1. In domain, model behavior through classes, methods, and class relationships.
2. Free functions are forbidden in domain.
3. One class per file is mandatory in domain.
4. If domain behavior grows beyond one class, split it into additional domain files instead of adding more free functions or multiple top-level classes to one file.
5. Module-level constants are allowed only when they support a domain class and do not become a parallel procedural API.
6. Helper logic that cannot justify a class does not belong in domain.
7. When one-class-per-file would be violated inside an anchor, the anchor must become a same-named package and each class must move to its own file inside that package.

### Layout Constraints

Every domain layer follow tactical DDD rules and includes this minimum layout:

The required domain anchors are mandatory as concepts, but large domains may modularize behind those anchors.

1. `entity` is the required anchor for entity-bearing domain concepts.
2. `value_object` is the required anchor for value objects and pure domain data carriers.
3. `service` is the domain-service anchor when policy or behavior spans multiple domain concepts.
4. `repository` exists only when a real domain-owned repository contract is part of the model.
5. Additional internal modules are allowed when they stay inside domain and still map clearly back to these anchors.
6. When domain modularizes behind these anchors, it must still follow the iron rule: classes only, no free functions, and one class per file.
7. Each anchor may be implemented either as a single file or as a same-named package.
8. If an anchor contains more than one domain class, package form is required for that anchor.
9. In package form, `__init__.py` is only the export seam for that anchor; domain classes still live one-per-file under the package.
10. Do not place free-standing domain classes directly under `domain/` outside one of the required anchors.

#### Python

```
<feature>/domain/
    - entity.py | entity/               # (REQ) entities
    - repository.py | repository/       # (FUN) repository ABC classes
    - service.py | service/             # (EXT) domain services
    - value_object.py | value_object/   # (REQ) value objects
```

When package form is used, keep the anchor name and push classes one-per-file behind it:

```
<feature>/domain/
    - entity/
        - __init__.py
        - order.py
        - order_item.py
    - value_object/
        - __init__.py
        - order_id.py
        - money.py
    - service/
        - __init__.py
        - pricing_policy.py
```

## Infrastructure

### Ownership

- external systems, runtime integrations, persistence, filesystem, network, subprocess, framework, and serialization details
- implementations of abstractions owned by `domain` or `application`
- technical-boundary translation
- may depend on `domain`, but not on `application` or `ui`

### Layout Constraints

Every infrastructure layer includes this minimum layout:

This is also a floor, not a cap. Larger integrations may split by external system, protocol, or adapter type as long as the work remains infrastructure-owned.

1. `repository` is the anchor when infrastructure implements repository contracts defined elsewhere.
2. Other infrastructure-owned technical concerns may add their own internal modules behind the owning anchor.
3. If repository implementation needs multiple files, use `repository/` rather than loose sibling files.
4. In package form, keep technical helpers behind the package and export only the minimum seam through `__init__.py` when needed.
5. Cross-layer consumers may import infrastructure symbols only through `infrastructure/__init__.py` or the owning anchor shim when infrastructure modularizes further.

#### Python

```
<feature>/infrastructure/
    - __init__.py                 # (FUN) factory functions for abstractions like repositories
    - repository.py | repository/ # (FUN) implements interfaces from domain layer
```

Example package form:

```
<feature>/infrastructure/
    - repository/
        - __init__.py
        - order_repository.py
        - order_mapper.py
```

## Application

- may be skipped if feature is upstream without usecases

### Ownership

- use cases, orchestration, workflow coordination, and feature-to-feature adaptation
- translation needed to execute a use case
- application-owned abstractions for outward capabilities
- may depend on `domain` and `infrastructure`, but not on `ui`

### Layout Constraints

Every application layer includes this minimum layout:

These anchors are the only allowed top-level ownership buckets inside `application/` under the shared default. Additional structure is allowed only behind these anchors, not as loose peer files or folders directly under `application/`.

1. `adapters` is the feature-to-feature adaptation anchor when cross-feature coordination is needed.
2. `services` is the orchestration anchor for reusable multi-step application coordination.
3. `commands` and `queries` are required anchors for write-side and read-side use-case entry points under the shared default.
4. `commands` and `queries` may each be implemented as a file or as a same-named package.
5. If multiple command handlers or query handlers are needed, package form is required for that anchor.
6. If reusable orchestration grows beyond one coherent file, keep it behind `services.py` or `services/`; do not introduce loose helper files directly under `application/`.
7. If cross-feature adaptation is needed, keep it behind `adapters/`; do not introduce loose feature-integration files directly under `application/`.
8. Do not leave command handlers, query handlers, orchestration helpers, read models, or other application-owned classes loose under `application/` outside the owning anchors.
9. Cross-layer consumers may import application symbols only through `application/__init__.py` or the owning anchor shim when application modularizes further.

#### Python

```
<feature>/application/
    - __init__.py
    - adapters/                     # (FUN) the one and only places to communicate with other features
        - __init__.py               # expose minimum API
        - other_feature_adapter.py  #
    - services.py | services/   # (EXT) reusable application orchestration only
        # package form when multiple owned service slices are needed
    - commands.py | commands/   # (REQ) write-side use cases
    - queries.py | queries/     # (REQ) read-side use cases
```

Example package form:

```
<feature>/application/
    - services/
        - __init__.py
        - build_report.py
        - runtime_selection.py
    - commands/
        - __init__.py
        - sync_project.py
        - bootstrap_workspace.py
    - queries/
        - __init__.py
        - describe_workspace.py
        - list_violations.py
```

## UI

- may be skipped when no user interaction are planned

### Ownership

- the outermost delivery layer
- command handlers, controllers, route handlers, presenters, renderers, and request or response mapping
- input collection, output formatting, and user-facing interaction concerns
- thin coordination only; business rules and workflow logic do not live here
- may depend only on `application`

### Layout Constraints

Every ui layer includes this minimum layout:

These anchors are the minimum delivery surface, not the only allowed files. Larger delivery code may add internal presenters, formatters, or request mappers inside ui.

1. `cli` is the command-binding anchor for CLI delivery.
2. `views` is the presentation-shaping anchor for delivery-specific view models or renderable payloads.
3. `services` is the delivery-helper anchor for UI-only support logic.
4. `cli`, `views`, and `services` may each be implemented as a file or as a same-named package.
5. If one delivery anchor needs multiple commands, presenters, or formatters, package form is required for that anchor.
6. Do not leave delivery helpers loose under `ui/` outside the owning delivery anchor.
7. `ui` may consume only application shims and may not deep-import application internals.

#### Python

```
<feature>/ui/
    - __init__.py
    - services.py | services/   # (EXT) helping services for delivery activities
    - views.py | views/         # (EXT) view objects or presentation models
    - cli.py | cli/            # (EXT) entrypoint for cli app
```

Example package form:

```
<feature>/ui/
    - cli/
        - __init__.py
        - check_command.py
        - update_command.py
    - views/
        - __init__.py
        - summary_view.py
        - violation_view.py
```