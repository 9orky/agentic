# Testing Rules

Use this document to define test strategy, test scope, fixtures, and local test structure.

Use the standard development run from `AGENT.md`.

Use `FEATURE.md` or `MODULE.md` to choose the correct public seam before writing tests.

Also read:

- `FEATURE.md` when the test exercises a feature boundary
- `MODULE.md` when the test exercises a module public API
- `REFACTORING.md` when the test is part of migration or caller swap work
- `PLANNING.md` when a plan step defines the verification contract

This document owns test-specific rules. If another document mentions tests, treat it as routing or acceptance context, not as a separate source of testing policy.

## Testing Goal

The role of tests is to check whether the code works as intended.

The role of tests is not to become green by any means necessary.

A passing test with weak assertions, the wrong seam, or a fake backdoor is a failed verification strategy.

## Core Rules

1. Test only public interfaces.
2. Test features through the feature boundary and modules through the module public API.
3. Prefer the highest public seam that proves the intended behavior.
4. Default to functional or boundary tests unless a narrower public seam is clearly the better fit.
5. Do not add test-only exports, hooks, flags, setters, or alternate production code paths.
6. If something is hard to test through the public seam, fix the design or choose the correct seam.

## Public Seam Rules

1. Test a feature through its public feature boundary.
2. Test a module through its public entry point or declared public API.
3. Do not deep-import internal files just to reach easier assertions.
4. Do not recreate private wiring in the test when the owner already exposes the correct boundary.
5. Import contract-owned data shapes and shared domain names instead of redefining parallel local types in fixtures.

## Choosing Test Level

1. Start at the public boundary that matches the user-visible intent.
2. Move to a narrower public seam only when it makes the behavior clearer or localizes failure meaningfully.
3. Do not drop below a public seam into file-private helpers or internal module internals.
4. When one behavior is already proven at the feature boundary, do not duplicate the same proof across multiple internal tests unless the extra coverage buys distinct signal.

## Test Directory Rules

1. Each local test directory or package must own a local helper file or small helper set.
2. Keep those helpers next to the tests they support.
3. Helpers should build valid requests, harnesses, and assertion helpers for that test area's public seam.
4. Helpers must remove setup noise, not hide the behavior under test.
5. Do not create a global dumping ground of generic test utilities when the helpers are really local to one test area.

## Helper Rules

1. Name helpers by domain intent, not by testing mechanics.
2. Keep helper outputs small and explicit enough that each test still reads like a specification.
3. Prefer one local helper file or a small helper set over repeated inline setup across many tests.
4. Promote repeated literals into named helper defaults only when the names make the scenario easier to read.
5. If a helper grows large enough to hide the scenario, split it or inline the case-specific data again.

## Fixture And Assertion Rules

1. Build the smallest valid input that proves the scenario.
2. Keep one test focused on one behavioral intent.
3. Assert observable outputs, contract shape, and business consequences.
4. Do not assert private state, helper usage, or incidental implementation order unless that order is itself part of the public contract.
5. Prefer explicit expected values over vague truthy checks when the contract can be stated concretely.

## Failure Rules

1. Code should fail early and loud on invalid input, invalid state, and broken assumptions.
2. When failure is the intended behavior, test it explicitly with a throws-style assertion or the equivalent error assertion for the test framework.
3. Assert the intended error, failure message, or failure shape instead of accepting any generic failure.
4. Keep failure cases first and the happy path last so the expected success path stays visually clear.
5. Do not hide expected failures behind broad catch blocks that weaken the signal of the test.

## Design Feedback Rules

1. If the test needs a production backdoor, stop and redesign the seam or the test approach.
2. If test setup is hard to read, improve the local helpers before adding more cases.
3. If failure assertions are hard to write, check whether the public contract is missing a clear failure mode.
4. Do not weaken assertions just to make a test pass more easily.
5. **Circuit Breaker**: If validation or test execution fails 2 times on the same boundary, STOP and ask for clarification. Do not engage in exhaustive trial-and-error.

## Acceptance Check

Before accepting test work, verify:

1. the public seam under test is named and intentional
2. no test-only production seam was added
3. helpers are local to the test area and keep test bodies readable
4. fixtures use owner-defined contracts and domain names
5. assertions prove the intended behavior rather than implementation trivia
6. failure cases, when relevant, check the intended error path explicitly
