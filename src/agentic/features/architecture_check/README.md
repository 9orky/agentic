# Architecture Check Config Guide

This feature validates an `agentic.yaml` or `agentic.yml` architecture agreement against an extracted dependency map.

This document is for developers writing or reviewing those config mappings.

The goal is not to describe every internal implementation detail. The goal is to help you write configs that stay:

- flexible enough to survive refactors
- scalable enough to cover many modules or features
- concise enough to remain understandable

## What The Checker Reads

The config surface is intentionally small:

```yaml
language: python | typescript | php

exclusions:
  - <glob>

rules:
  boundaries:
    - source: <pattern>
      disallow:
        - <pattern>
      allow:
        - <pattern>
      allow_same_match: true | false

  tags:
    - name: <tag-name>
      match: <pattern>

  flow:
    layers:
      - <tag-name>
    module_tag: <tag-name>
    analyzers:
      - backward-flow
      - no-reentry
      - no-cycles
```

## Matching Semantics

The checker normalizes paths to `/` separators.

Patterns support:

- `*` for one path segment capture
- `**` for multi-segment capture
- `?` for one character within a segment

Important behavior:

- boundary `source` patterns are matched in scope mode
- boundary `disallow` patterns are matched in scope mode
- boundary `allow` patterns are matched in exact mode
- tag `match` patterns are matched in scope mode

That means the checker is good at expressing:

- broad deny rules over whole owned areas
- narrow exceptions for exact public seams such as a feature root, layer shim, or anchor shim

In practice this means:

- `source: src/features/orders` matches `src/features/orders` and everything below it
- `disallow: src/features/billing` matches `src/features/billing` and everything below it
- `allow: src/features/billing` allows only the exact seam path match, not `src/features/billing/internal/...`

That exact-vs-scope distinction is what lets one rule say:

- deny cross-feature internal imports broadly
- allow exact public seams narrowly

## Writing Good Configs

### Prefer Stable Architectural Seams

Write mappings against stable ownership boundaries, not volatile file names.

Prefer this:

```yaml
rules:
  boundaries:
    - source: src/features/*/ui
      disallow:
        - src/features/*/domain
        - src/features/*/infrastructure
```

Avoid this:

```yaml
rules:
  boundaries:
    - source: src/features/orders/ui/cli.py
      disallow:
        - src/features/orders/domain/entity/order.py
```

The first survives internal refactors. The second will rot immediately.

### Use One Broad Rule Before Many Narrow Ones

Start with the broadest rule that captures the architectural intent.

Example:

```yaml
rules:
  boundaries:
    - source: src/features/*/ui
      disallow:
        - src/features/*/domain
        - src/features/*/infrastructure
```

This scales better than writing the same rule once per feature.

### Use `allow_same_match` To Avoid Rule Explosion

If two wildcard patterns capture the same owning slice, `allow_same_match: true` allows imports where the captures are equal.

Example:

```yaml
rules:
  boundaries:
    - source: src/features/*
      disallow:
        - src/features/*
      allow_same_match: true
```

This means:

- `orders -> orders` is allowed
- `orders -> billing` is denied

This is the main tool for expressing scalable "same owner allowed, other owner denied" rules.

### Use `allow` Only For Narrow Public Seams

Because `allow` is exact-match only, it is best used for public entry points.

Example:

```yaml
rules:
  boundaries:
    - source: src/features/*
      disallow:
        - src/features/*
      allow_same_match: true
      allow:
        - src/features/*
```

This combination means:

- same-feature imports remain allowed
- exact feature-root imports remain allowed
- deep imports into another feature remain denied

That pattern is concise and usually more maintainable than enumerating every allowed public file.

### Model Layer And Anchor Shims Explicitly

If a codebase routes cross-layer imports through layer shims or anchor shims, the config must allow those exact seam paths.

Example:

```yaml
rules:
  boundaries:
    - source: src/features/*/ui
      disallow:
        - src/features/*/application
        - src/features/*/domain
        - src/features/*/infrastructure
      allow:
        - src/features/*/application
        - src/features/*/application/commands
        - src/features/*/application/queries
        - src/features/*/application/services
```

This does not grant access to arbitrary application internals. It grants access only to the exact exported seams that UI is allowed to import.

### Exclude Noise Early

Use `exclusions` to remove generated, vendored, or irrelevant code before writing boundary rules.

Example:

```yaml
exclusions:
  - tests/**
  - node_modules/**
  - dist/**
  - build/**
  - .venv/**
  - generated/**
```

Good exclusions keep the config focused on architecture, not tool output.

### Use Tags For Flows, Not For Everything

Tags are useful when the rule is about role or layer ordering rather than direct path denies.

Use tags when you want rules like:

- features may depend on modules and adapters, but not backward
- modules must not re-enter through another module
- layers must move in one direction only

Do not use tags for simple direct boundaries when one `boundaries` rule is enough.

## Recommended Authoring Strategy

### 1. Start With Exclusions

Remove directories that should never influence architecture discussion.

### 2. Encode Hard Boundaries First

Write the direct dependency rules that must never be broken.

Examples:

- `ui` must not import `domain`
- `domain` must not import `infrastructure`
- one feature must not deep-import another feature

### 3. Add Public-Seam Exceptions

If broad rules block legitimate seam imports, add narrow `allow` entries.

### 4. Add Flow Rules Only When Needed

If direct boundaries are not enough to express the architectural intent, add tags plus flow analyzers.

### 5. Stop When The Intent Is Clear

A config that is shorter and obviously architectural is better than a config that describes the filesystem exhaustively.

## Practical Examples

### Example 1: Simple Layered Slice

```yaml
language: python

exclusions:
  - tests/**
  - .venv/**

rules:
  boundaries:
    - source: src/domain
      disallow:
        - src/infra

    - source: src/ui
      disallow:
        - src/domain
        - src/infra
```

Use this style when the architecture is small and direct path rules are enough.

### Example 2: Same-Feature Allowed, Cross-Feature Denied

```yaml
language: python

rules:
  boundaries:
    - source: src/features/*
      disallow:
        - src/features/*
      allow_same_match: true
      allow:
        - src/features/*
```

Use this style when each feature may use its own internals but other features may only use the public seam.

### Example 3: Feature Layer Rules At Scale

```yaml
language: python

rules:
  boundaries:
    - source: src/features/*/ui
      disallow:
        - src/features/*/application
        - src/features/*/domain
        - src/features/*/infrastructure
      allow:
        - src/features/*/application
        - src/features/*/application/commands
        - src/features/*/application/queries
        - src/features/*/application/services

    - source: src/features/*/application
      disallow:
        - src/features/*/ui
        - src/features/*/domain
        - src/features/*/infrastructure
      allow:
        - src/features/*/domain
        - src/features/*/domain/entity
        - src/features/*/domain/value_object
        - src/features/*/domain/service
        - src/features/*/infrastructure

    - source: src/features/*/infrastructure
      disallow:
        - src/features/*/ui
        - src/features/*/application
        - src/features/*/domain
      allow:
        - src/features/*/domain
        - src/features/*/domain/entity
        - src/features/*/domain/value_object
        - src/features/*/domain/service

    - source: src/features/*/domain
      disallow:
        - src/features/*/ui
        - src/features/*/application
        - src/features/*/infrastructure
```

Use this style when the same layer contract repeats across many features and cross-layer imports are required to pass through exact shims instead of deep module paths.

### Example 4: Flow Rules For Directional Movement

```yaml
language: python

rules:
  boundaries: []
  tags:
    - name: feature
      match: src/features/**
    - name: module
      match: src/modules/**
    - name: adapter
      match: src/adapters/**
  flow:
    layers:
      - feature
      - module
      - adapter
    module_tag: module
    analyzers:
      - backward-flow
      - no-reentry
      - no-cycles
```

Use this style when the question is about directional topology, not just pairwise deny lists.

## How To Keep Configs Scalable

### Prefer Captures Over Enumeration

Prefer:

```yaml
source: src/features/*/ui
```

Over:

```yaml
source: src/features/orders/ui
source: src/features/billing/ui
source: src/features/users/ui
```

### Prefer Architectural Names Over Tool Names

Prefer tags like:

- `feature`
- `module`
- `adapter`
- `public_seam`

Avoid tags that only mirror transient implementation details.

### Keep Each Rule About One Idea

One boundary rule should usually express one architectural statement.

Good:

```yaml
- source: src/features/*/ui
  disallow:
    - src/features/*/domain
```

Less good:

```yaml
- source: src/features/*/ui
  disallow:
    - src/features/*/domain
    - src/shared/generated
    - src/framework
    - vendor
    - tools/tmp
```

If a rule mixes unrelated concerns, split it.

## Common Mistakes

### Mistake 1: Using Exact Allows As If They Were Scoped

This does not allow internals below the path:

```yaml
allow:
  - src/features/*
```

It allows only the exact matched seam path.

That is usually correct for public seam imports.

### Mistake 2: Forgetting Anchor Shims

If `ui` is allowed to import `application/services`, then `application/services` must appear explicitly in `allow`.

Allowing only `application` does not implicitly allow `application/services`.

### Mistake 3: Encoding Every File Instead Of The Boundary

If you need dozens of file-level rules, the config is probably modeling implementation details rather than architecture.

### Mistake 4: Skipping Exclusions

Generated or vendored files will create noise and false architectural debates.

### Mistake 5: Using Flow Tags Without Stable Tag Meanings

If `module` or `feature` is not semantically stable in the codebase, flow analysis will become confusing.

## Review Checklist

Before committing a config change, ask:

- Does each rule describe an architectural boundary rather than a temporary file arrangement?
- Can repeated rules be collapsed into wildcard captures?
- Are public seam exceptions explicit and narrow?
- Are exclusions removing irrelevant code?
- Are flow tags semantically stable and easy to explain?
- Could another developer understand why each rule exists without reverse-engineering the whole repo?

## Suggested Next Step

Write the smallest config that expresses the intended architecture, run the checker, then tighten only the places where the first draft is too permissive or too noisy.

That sequence usually produces a config that is both concise and durable.