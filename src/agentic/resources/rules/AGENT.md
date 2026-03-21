# Agent Rules

`agentic` packages a rules tree that an agent can navigate step by step instead of loading as one flat document set.

Read this file first. Then follow one markdown link to the governing bootstrap file for the current task.

## Available Rule Sets

| Rule Set | Information You Can Obtain | Bootstrap |
| --- | --- | --- |
| Rules maintenance | how the packaged rules tree should be navigated, split, and kept under continuous refinement | [../README.md](../README.md) |
| Feature rules | which feature layer owns a responsibility and which next layer document can resolve placement questions | [feature/FEATURE.md](feature/FEATURE.md) |
| Planning rules | which planning stage applies now and which planning document gives the next level of detail | [planning/PLANNING.md](planning/PLANNING.md) |
| Module rules | the module-boundary rules that define public seams, private internals, and dependency direction | [module/MODULE.md](module/MODULE.md) |
| Refactoring rules | the target-design refactoring rules and whether placement questions must route into feature guidance | [refactoring/REFACTORING.md](refactoring/REFACTORING.md) |
| Testing rules | the verification rules for choosing seams, assertions, helpers, and test scope | [tests/TESTS.md](tests/TESTS.md) |

## Navigation Rule

1. Read only the document you are in.
2. Follow only the next link that matches the task.
3. If that document offers child options, choose from those options there.
4. Do not skip across the tree without a link from the current document.

## Local Bootstrap

If the task is to bootstrap or refresh the local `agentic/` guidance entrypoint in a project, use [../README.md](../README.md) to obtain:

1. the cleanup rule for existing project instructions and caches
2. the default location for the bootstrap instruction file
3. the exact minimal markdown text to place there