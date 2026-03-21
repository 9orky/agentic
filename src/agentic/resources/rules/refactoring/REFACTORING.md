# Refactoring Rules

Use this file when reshaping existing code or replacing an existing structure.

If the task raises placement or ownership ambiguity, use [../feature/FEATURE.md](../feature/FEATURE.md) to obtain the next valid feature links and then follow only the layer document that resolves that ambiguity.

## Core Rules

1. Start from the target design, not the current structure.
2. Keep the target design as simple as the accepted outcome allows.
3. Treat existing callers as behavioral reference only.
4. Keep the public API intact unless the user or approved plan changes it.
5. Preserve or strengthen the owning feature enclosure.
6. Refactor toward the governing feature anatomy for the current project.
7. Place every touched file, type, and responsibility in its owning part.
8. Do not preserve legacy architectural buckets as a shortcut.
9. Use a fresh slice when ownership, boundaries, or structure change substantially.
10. Delete migration scaffolding after the canonical path is active and verified.

## Execution Pattern

1. Confirm the target enclosure, public boundary, public seam, and governing feature anatomy.
2. Decide between in-place refactor and a fresh slice.
3. Move each touched file and type by ownership, not by legacy file names.
4. Verify through the intended public boundary and public seam before swapping callers.
5. Delete the legacy path only after the new path is active and verified.

## Constraints

1. Do not mutate legacy structure in place when the target design needs a fresh slice.
2. Do not add helper exports or public shims to preserve accidental callers.
3. Do not collapse responsibilities into the public boundary as a shortcut.
4. Do not blur ownership or spread feature growth beyond the enclosure.

## Verification

Before accepting a refactor step, verify:

1. public behavior through the intended boundary first
2. helper internals do not leak through exports
3. explicit inputs still mean what they say
4. every touched file belongs clearly to the owning layer
5. dependency direction remains valid across the touched parts