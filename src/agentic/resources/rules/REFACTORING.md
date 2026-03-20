# Refactoring

Use this document when reshaping existing code or replacing an existing structure.

## Core Rules

1. Start from the target design, not the current structure.
2. Keep the target design as simple as the accepted outcome allows.
3. Treat existing callers as behavioral reference only.
4. Keep the public API intact unless the user or approved plan changes it.
5. Preserve or strengthen the owning feature enclosure.
6. Refactor toward the governing feature anatomy for the current project.
7. Place every touched file, type, and responsibility in its owning part.
8. Under the shared default, do not preserve root-level architectural buckets such as `contracts`, `ports`, `adapters`, `services`, `types`, or `utils` as a shortcut.
9. Use a fresh `_refactor` or `_refactored` slice when ownership, boundaries, or structure change substantially.
10. Delete completed migration scaffolding after the canonical path is active and verified.

## Execution Pattern

1. Confirm the target enclosure, public boundary, public seam, and active feature anatomy.
2. Decide between in-place refactor and fresh slice.
3. Move each touched file and type by ownership, not by legacy file names.
4. Under the shared default, keep cross-feature coordination in `application`, external integrations in `infrastructure`, user-facing delivery in `ui`, and business rules in `domain`.
5. Keep unfinished downstream wiring behind local placeholders in the correct owning part.
6. Verify through the intended public boundary and public seam before swapping callers.
7. Promote the new slice to the canonical path.
8. Delete the legacy slice only after the new path is active and verified.

If the current structure already matches the target public boundary and the change is small, refactor in place.

## Constraints

1. Do not mutate legacy structure in place when the target design needs a fresh slice.
2. Do not add helper exports or public shims to preserve accidental callers.
3. Do not collapse responsibilities into the public boundary as a shortcut.
4. Do not silently merge explicit caller configuration with defaults unless the contract documents merge semantics.
5. Do not implement later-phase behavior early unless the approved scope changes.
6. Do not replace the target design with branchy temporary scaffolding just to get a green result.
7. Cross-boundary fixes require plan amendment or explicit approval.
8. Do not blur ownership or spread feature growth beyond the enclosure.
9. Under the shared default, do not keep a legacy root bucket alive just because the old code used it.
10. Do not let current file names override ownership in the governing anatomy.
11. Do not treat a badly designed feature as a special case when the governing rules are clear.
12. If the project appears to use a stable different anatomy but the local docs do not define it, stop and document or confirm that anatomy before structural refactoring.

## Placeholders

Use placeholders only when they state unfinished wiring without pretending the behavior is complete.

1. State what final wiring is still required.
2. Keep the placeholder inside the owning slice unless it is the deliberate public seam of the target boundary being prepared.
3. Do not fake success, hide branching, or mimic finished behavior.
4. Make the placeholder easy to replace.
5. If it would become a long-lived boundary, stop and ask.

## Verification

Before accepting a refactor step, verify:

1. public behavior through the intended public boundary and public seam first
2. helper internals do not leak through exports
3. explicit inputs still mean what they say after normalization
4. the result still matches the approved plan when one exists
5. the owning enclosure is still clear and intact, and growth remains inside it
6. every touched file belongs clearly to the owning part defined by the governing feature anatomy
7. dependency direction remains valid across the touched parts