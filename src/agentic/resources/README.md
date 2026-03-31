# Resources Guide

This directory is the packaged source of truth for the shared rule system shipped by `agentic`.

Use this README when the task is about changing the rule sets themselves, not when the task is about following one of the rule sets during normal work.

## How To Navigate The Rules Tree

1. Start in [rules/INDEX.md](rules/INDEX.md) to obtain the available rule sets and the next valid links.
2. Follow one markdown link to the governing bootstrap file.
3. If that bootstrap file offers child documents, choose one of those child links there.
4. Continue step by step instead of skipping across the tree.

## Agent Navigation And Discovery Guidelines

Manage the rules tree so an agent can discover the governing rule set with the fewest possible decisions and without loading unrelated detail.

Guidelines:

1. keep discovery at the router level and detailed guidance at the leaf level
2. make the next valid link explicit instead of expecting the agent to infer the next document
3. keep one rule set responsible for one concern, then link outward when another concern becomes governing
4. make document purpose legible from its title, headings, and link table before any detailed reading begins
5. keep the same discovery path stable over time unless the old path has become noisy, leaky, or ambiguous
6. when adding a new rule split, update the parent router so the agent can discover it through normal navigation rather than by coincidence
7. if a task needs another rule set, link to that rule set instead of restating its detailed rules locally
8. keep shared rule docs tech-stack agnostic; do not name specific languages, frameworks, runtimes, package managers, or delivery/execution technologies in packaged rule docs, and place stable stack-specific guidance only in repo-local overrides or project-specific docs

The goal is not only clean documentation. The goal is reliable agent routing: the agent should be able to identify the current governing rule set, the next valid document, and the stopping point for loaded detail without guesswork.

## Router Versus Leaf

Router documents exist to send the reader to the next document.

Router documents should contain:

1. a short definition of the current rule set
2. a table or list of next documents
3. markdown links to those documents
4. a short explanation of when or why to follow each link

Router documents should not contain:

1. detailed rules that belong in child documents
2. restated summaries of downstream documents
3. hidden assumptions about unrelated rule sets
4. navigation that jumps across the tree without explanation

Leaf documents hold the detailed rules for one concern.

## How To Split A Rule Set

Split a rule set further when its current document stops being a clean leaf and starts mixing multiple concerns.

When splitting:

1. keep the existing bootstrap file as the entrypoint for that rule set
2. move detailed rules into child documents
3. leave only selection guidance and child links in the bootstrap file
4. keep links explicit and local to the next level

Every split is provisional. The rules tree is expected to stay under continuous refinement and refactoring as better navigation patterns emerge.

## Maintenance Risks

The risks below are standing guidance and should stay visible whenever the packaged rule system is edited.

1. over-splitting can create too many hops and make discovery worse
2. under-splitting preserves the context-window problem that the navigation model is meant to solve
3. router bloat makes INDEX.md or a bootstrap file drift back into a rules dump
4. abstraction leaks happen when one rule set embeds another rule set's detailed logic instead of linking to it
5. duplicated manifests of the packaged rules tree create drift; when code needs the tree shape, enumerate the packaged source-of-truth tree directly instead of copying file lists into multiple places
6. tech-specific wording in shared rules makes the default contract less reusable and pushes package behavior toward one stack instead of a general architecture model

Treat these risks as active maintenance pressure. The correct structure is not fixed permanently. It should be refined whenever the navigation model becomes noisy, leaky, or harder to supervise.

## Heavy Violations

Treat the cases below as heavy violations when editing the packaged rules tree.

1. a router document or bootstrap file explains the detailed content of another rule set instead of linking to it
2. a rule document mixes discovery for one concern with detailed instructions owned by a different rule set
3. a parent document removes the agent's need to navigate by embedding downstream detail inline
4. a new rule set is added without making it discoverable from its governing router

These violations are heavy because they break the navigation model itself. They make discovery ambiguous, increase context noise, and cause the agent to load the wrong detail at the wrong level.

## Local Agentic Bootstrap

When a project needs a local bootstrap instruction that points the agent toward the `agentic/` folder, keep that instruction minimal and manage it at one default location.

The workspace-contract behavior uses this default location:

- `.github/copilot-instructions.md`

The deterministic behavior is:

1. `agentic init` creates the file when it is missing
2. `agentic update` restores the file to the packaged default text
3. the file must contain only the minimal pointer below rather than inline rule detail

Place exactly this markdown text in that file:

```md
# agentic

Go to the `agentic/` folder and explore it. You will find the project guidance there.
```

That bootstrap text must stay minimal. It should not expose rule details inline. It should only direct the agent to the local `agentic/` folder, where the navigable guidance already exists.