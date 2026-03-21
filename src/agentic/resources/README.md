# Resources Guide

This directory is the packaged source of truth for the shared rule system shipped by `agentic`.

Use this README when the task is about changing the rule sets themselves, not when the task is about following one of the rule sets during normal work.

## How To Navigate The Rules Tree

1. Start in [rules/AGENT.md](rules/AGENT.md) to obtain the available rule sets and the next valid links.
2. Follow one markdown link to the governing bootstrap file.
3. If that bootstrap file offers child documents, choose one of those child links there.
4. Continue step by step instead of skipping across the tree.

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
3. router bloat makes AGENT.md or a bootstrap file drift back into a rules dump
4. abstraction leaks happen when one rule set embeds another rule set's detailed logic instead of linking to it

Treat these risks as active maintenance pressure. The correct structure is not fixed permanently. It should be refined whenever the navigation model becomes noisy, leaky, or harder to supervise.

## Local Agentic Bootstrap

When a project needs a local bootstrap instruction that points the agent toward the `agentic/` folder, keep that instruction minimal.

Before writing it:

1. clean the current project-level `agentic` instructions
2. clean any cached copies of those old instructions
3. define one default location for the bootstrap instruction instead of scattering multiple variants across the project

The default location for that bootstrap instruction is:

- `.github/copilot-instructions.md`

Place exactly this markdown text in that file:

```md
# agentic

Go to the `agentic/` folder and explore it. You will find the project guidance there.
```

That bootstrap text must stay minimal. It should not expose rule details inline. It should only direct the agent to the local `agentic/` folder, where the navigable guidance already exists.