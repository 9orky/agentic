# Feature Rules

Document Class: navigational

## Purpose

A feature owns one business capability, one public boundary, and the modules that live inside that boundary.

## Use This When

1. Use this file when the task needs feature-shape or feature-to-module ownership guidance.
2. Read the child module document when the task needs module or layer detail.

## Available Options

| Document | Information You Can Obtain |
| --- | --- |
| [module/MODULE.md](module/MODULE.md) | the feature-internal module routing contract that decides which module owns the responsibility and then routes to that module's layer rules |

## Navigation Rule

1. Stay in this document until the owning feature is clear.
2. Follow only the module link that resolves which module owns the responsibility.
3. Do not infer layer placement here when the feature-module document can route that question directly.

## Local Context

Under the shared default, a feature is organized through modules.

Each module owns its own layer set:

1. `domain`
2. `infrastructure`
3. `application`
4. `ui`

## Exit Condition

1. You have identified that the question is inside one feature boundary.
2. The next read is [module/MODULE.md](module/MODULE.md).