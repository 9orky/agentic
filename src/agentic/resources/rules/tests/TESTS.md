# Testing Rules

Document Class: leaf

## Purpose

Use this document to define test strategy, scope, helpers, fixtures, and assertions.

## Applies When

Read the governing feature or module bootstrap file first when the test needs architecture-specific placement context.

## Scope

This file governs which public seam to test, how to structure assertions, and how to keep tests aligned with the owning enclosure.

## Core Rules

### Default Strategy

1. Default to functional or boundary tests at the feature public boundary through its public seam.
2. Test a module directly only when the module itself owns the relevant public boundary or the narrower public seam gives clearer signal.
3. Prefer the highest public boundary and public seam that prove the behavior.
4. Do not duplicate the same proof at lower seams unless the extra test gives distinct signal.
5. Let tests reinforce the owning enclosure by proving behavior through its intended public boundary and public seam.

### Core Rules

1. Test only public interfaces.
2. Do not add test-only exports, hooks, flags, setters, or alternate production paths.
3. Do not deep-import internal files or recreate private wiring in tests.
4. If something is hard to test through the public seam, fix the design or choose the correct seam.
5. Use owner-defined contracts and shared domain names in fixtures instead of redefining parallel local types.
6. Do not weaken an enclosure in tests just to make internal behavior easier to reach.

## Constraints

### Test Shape

1. Build the smallest valid input that proves the scenario.
2. Keep one test focused on one behavioral intent.
3. Put negative cases first and the happy path last.
4. Assert observable outputs, contract shape, and business consequences.
5. Do not assert private state or incidental implementation order unless it is part of the public contract.

### Helpers

1. Keep helpers local to the test area they support.
2. Name helpers by domain intent, not testing mechanics.
3. Use helpers to remove setup noise, not hide behavior.

## Acceptance Check

1. The public seam under test is named and intentional.
2. The public boundary under test is named and intentional.
3. No test-only production seam was added.
4. Helpers are local and keep tests readable.
5. Assertions prove behavior, not implementation trivia.