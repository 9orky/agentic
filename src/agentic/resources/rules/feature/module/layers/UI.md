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

### Layout Constraints

Use these anchors as the minimum delivery surface:

1. one entrypoint anchor
2. `views`
3. `services`

Each anchor may be a file or a same-named package. If an anchor needs multiple delivery handlers or presenters, switch it to package form.

## Constraints

### Placement Rules

1. Keep business rules and workflows out of `ui`.
2. Do not deep-import application internals.
3. Keep delivery helpers behind the owning UI anchor instead of as loose files.

## Acceptance Check

1. `ui` depends only on application seams.
2. Delivery logic stays in `ui` and business logic stays out.
3. No loose helper files spill outside the owning anchor.