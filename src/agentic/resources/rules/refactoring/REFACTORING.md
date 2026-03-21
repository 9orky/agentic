# Refactoring Rules

Use this file when reshaping existing code or replacing an existing structure.

If the task raises placement or ownership ambiguity, use [../feature/FEATURE.md](../feature/FEATURE.md) to obtain the next valid feature links and then follow only the layer document that resolves that ambiguity.

## Core Rules

1. Start from the target design, not the current structure.
2. Keep the target design as simple as the accepted outcome allows.
3. Treat the current feature as weak behavioral reference only.
4. Keep the public API intact unless the user or approved plan changes it.
5. Preserve or strengthen the owning feature enclosure.
6. Refactor toward the governing feature anatomy for the current project.
7. Place every touched file, type, and responsibility in its owning part.
8. Do not preserve legacy architectural buckets as a shortcut.
9. Use a fresh slice when ownership, boundaries, or structure change substantially.
10. When doing a fresh-slice refactor of a feature, create a separate folder named exactly `<feature_name>_refactor`.
11. A separate `<feature_name>_refactor` folder means a fresh start rather than incremental repair inside the legacy feature folder.
12. Use the planning rule set for plan structure, planning stages, and plan artifact details during that fresh-slice refactor.
13. After the refactor is complete and verified through the intended boundary, swap the folders so the refactored folder becomes canonical and remove the legacy folder.
14. Delete migration scaffolding after the canonical path is active and verified.

## Execution Pattern

1. Confirm the target enclosure, public boundary, public seam, and governing feature anatomy.
2. Decide between in-place refactor and a fresh slice.
3. If the refactor is a fresh slice, create `<feature_name>_refactor` and use the planning rule set to establish the required planning artifacts before implementation starts.
4. Build the refactor inside `<feature_name>_refactor` as a new feature slice, using the current feature only as weak behavioral reference.
5. Move each touched file and type by ownership, not by legacy file names.
6. Verify through the intended public boundary and public seam before swapping folders.
7. Swap the refactored and legacy folders only after the new path is active and verified.
8. Remove the legacy folder after the swap is complete.

## Constraints

1. Do not mutate legacy structure in place when the target design needs a fresh slice.
2. Do not add helper exports or public shims to preserve accidental callers.
3. Do not collapse responsibilities into the public boundary as a shortcut.
4. Do not blur ownership or spread feature growth beyond the enclosure.
5. Do not duplicate a packaged resource tree, rules tree, or filesystem contract as a second hardcoded manifest when the source-of-truth tree can be enumerated directly.
6. Do not treat the legacy feature folder as architectural authority during a fresh-slice refactor.
7. Do not skip the `<feature_name>_refactor` folder when the refactor is being executed as a fresh start.
8. Do not keep both legacy and refactored feature folders active after the verified swap.

## Verification

Before accepting a refactor step, verify:

1. public behavior through the intended boundary first
2. helper internals do not leak through exports
3. explicit inputs still mean what they say
4. every touched file belongs clearly to the owning layer
5. dependency direction remains valid across the touched parts