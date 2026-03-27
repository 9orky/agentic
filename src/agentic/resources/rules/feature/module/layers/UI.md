# UI Layer Rules

Document Class: leaf

## Purpose

Within the owning module, `ui` owns delivery entrypoints, request and response mapping, and presentation shaping.

## Applies When

Read this file when the task affects input binding, delivery coordinators, presenters, input shaping, or output shaping inside the current module.

## Ownership

`ui` owns:

1. delivery entrypoints
2. input and output mapping
3. presentation shaping and view models
4. delivery-specific helper logic

`ui` may depend only on `application`.

## Core Rules

### Required Anchors

Use these anchors as the minimum delivery surface:

1. one delivery entrypoint anchor
2. `views`
3. `services`

Do not leave loose UI-owned helper files at the layer root outside those anchors.

### Layout Constraints

1. The delivery entrypoint anchor may be a single file or a same-named package.
2. `views` owns presentation shaping, view models, and rendered output helpers.
3. `services` owns UI-local presenters, path formatters, or other delivery-only helper classes.
4. If an anchor needs multiple delivery handlers or presenters, switch it to package form.
5. Cross-layer consumers may import UI symbols only through `ui/__init__.py` or the owning anchor shim.

## Constraints

### Placement Rules

1. Keep business rules and workflows out of `ui`.
2. Import application only through the application layer shim or an explicitly approved application anchor shim.
3. Do not deep-import files inside another layer just to reach a concrete query, service, DTO, or helper.
4. Keep request parsing, argument binding, and response shaping in `ui`, not in `application`.
5. Keep delivery helpers behind the owning UI anchor instead of as loose files.

## Acceptance Check

1. `ui` depends only on application seams.
2. No cross-layer import from `ui` reaches deeper than the target application layer shim or approved anchor shim.
3. Delivery logic stays in `ui` and business logic stays out.
4. The delivery entrypoint, `views`, and `services` remain the only root UI anchors under the shared default.
5. No loose helper files spill outside the owning anchor.