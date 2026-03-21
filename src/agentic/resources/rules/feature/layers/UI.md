# UI Layer Rules

Read this file when the task affects command binding, controllers, presenters, request parsing, or response formatting.

## Ownership

`ui` owns:

1. CLI or endpoint entrypoints
2. request and response mapping
3. presentation shaping and view models
4. delivery-specific helper logic

`ui` may depend only on `application`.

## Layout Constraints

Use these anchors as the minimum delivery surface:

1. `cli`
2. `views`
3. `services`

Each anchor may be a file or a same-named package. If an anchor needs multiple delivery handlers or presenters, switch it to package form.

## Placement Rules

1. Keep business rules and workflows out of `ui`.
2. Do not deep-import application internals.
3. Keep delivery helpers behind the owning UI anchor instead of as loose files.

## Acceptance Check

1. `ui` depends only on application seams.
2. Delivery logic stays in `ui` and business logic stays out.
3. No loose helper files spill outside the owning anchor.