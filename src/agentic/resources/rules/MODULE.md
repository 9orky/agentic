# Module Rules

A module has one public boundary reached through one public seam.

Inside a feature, module boundaries support the owning enclosure. They allow internal growth and composition, but they do not replace or widen the governing feature anatomy.

The governing feature anatomy is the shared default in `FEATURE.md` unless a repo-local override replaces it.

## Form

1. Use a single file while the module is simple.
2. Convert the module to a folder only when private composition is needed.
3. A folder module is composition behind one public seam.
4. Do not create a folder before there is private structure to hide.

## Public API

1. Expose the minimum public API.
2. Widen it only when multiple external consumers need it or an approved plan requires it.
3. Do not widen it to avoid local wiring work.
4. Callers import through the public seam only.
5. Do not use a module API to bypass or dilute the owning feature boundary.

## Internals

1. Keep helpers, policies, services, and intermediate models private.
2. Split internal parts by responsibility.
3. Deep imports into internal files are forbidden.

## Dependencies

1. Dependencies stay directional.
2. Circular dependencies are forbidden.
3. A parent may depend on a child module's public seam only.
4. A child must not depend on its consumer.
5. Inside a feature, module dependencies must also respect the dependency direction of the governing feature anatomy.

## Acceptance Check

1. The module uses the simplest valid form.
2. The public boundary and public seam are clear.
3. Public API is minimal.
4. Internal files stay private.
5. No caller needs a deep import.
6. The module boundary reinforces the governing feature anatomy and owning enclosure by containing growth instead of spreading it.