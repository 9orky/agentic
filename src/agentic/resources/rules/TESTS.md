# Testing Rules

Use this document to define test strategy, scope, helpers, fixtures, and assertions.

Use the public boundary and public seam defined by the governing feature anatomy for the current project.

## Default Strategy

1. Default to functional or boundary tests at the feature public boundary through its public seam.
2. Test a module directly only when the module itself owns the relevant public boundary or the narrower public seam gives clearer signal.
3. Prefer the highest public boundary and public seam that prove the behavior.
4. Do not duplicate the same proof at lower seams unless the extra test gives distinct signal.
5. Let tests reinforce the owning enclosure by proving behavior through its intended public boundary and public seam.

## Core Rules

1. Test only public interfaces.
2. Do not add test-only exports, hooks, flags, setters, or alternate production paths.
3. Do not deep-import internal files or recreate private wiring in tests.
4. If something is hard to test through the public seam, fix the design or choose the correct seam.
5. Use owner-defined contracts and shared domain names in fixtures instead of redefining parallel local types.
6. Do not weaken an enclosure in tests just to make internal behavior easier to reach.
7. Do not use tests to force the shared default anatomy onto a project that documents a different local anatomy.

## Test Shape

1. Build the smallest valid input that proves the scenario.
2. Keep one test focused on one behavioral intent.
3. Put negative cases first and the happy path last.
4. Assert observable outputs, contract shape, and business consequences.
5. Do not assert private state or incidental implementation order unless it is part of the public contract.

## Helpers

1. Treat helper design as part of the test suite.
2. Keep helpers local to the test area they support.
3. Name helpers by domain intent, not testing mechanics.
4. Use helpers to remove setup noise, not hide behavior.
5. Do not create a generic dumping ground of global test utilities for local needs.

## Failure Rules

1. Test expected failures explicitly.
2. Assert the intended error, message, or failure shape instead of any generic failure.
3. Do not hide expected failures behind broad catch blocks.
4. If the test needs a production backdoor, redesign the seam or the test approach.
5. Follow the `AGENT.md` circuit-breaker rule when the same boundary or tactic fails twice.

## Acceptance Check

1. The public seam under test is named and intentional.
2. The public boundary under test is named and intentional.
3. No test-only production seam was added.
4. Helpers are local and keep tests readable.
5. Fixtures use owner-defined contracts and domain names.
6. Assertions prove behavior, not implementation trivia.
7. The test approach preserves the governing feature anatomy and owning enclosure and does not normalize spreading beyond it.