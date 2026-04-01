# Architecture Check

The architecture-check feature validates an `agentic.yaml` or `agentic.yml` agreement against an extracted dependency map.

## Main Commands

- `agentic check`: run the architecture check and report violations
- `agentic hotspots`: show file import hotspot counts from the same dependency graph

## What It Validates

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

## Matching Semantics That Matter Most

- Path separators are normalized to `/`.
- Boundary `source` and `disallow` patterns are matched in scope mode.
- Boundary `allow` patterns are matched in exact mode.
- Tag `match` patterns are matched in scope mode.

That exact-versus-scope distinction is what makes broad boundary rules and narrow public-seam exceptions work together.

## Authoring Guidance

- Prefer stable architectural seams over file-specific paths.
- Start with broad boundary rules before adding narrow exceptions.
- Use `allow_same_match` when same-owner imports should stay legal under wildcard captures.
- Use tags and flow analyzers only when direct boundary rules are not enough.
- Exclude generated or vendored code early so the dependency graph stays meaningful.

## Limits

- The checker relies on extractor implementations whose fidelity can vary by language.
- Read and traversal failures can still fail the check explicitly.
- This page is the user-facing feature guide, not the exhaustive implementation reference.

## Related Docs

- [workspace-contract.md](/Users/gorky/Projects/agentic/docs/runtime/workspace-contract.md) for the generated contract surface
- [../architecture/mapping.md](/Users/gorky/Projects/agentic/docs/architecture/mapping.md) for the current repository architecture map

## Source Inputs

- [docs/architecture-mapping.md](/Users/gorky/Projects/agentic/docs/architecture-mapping.md)
- [src/agentic/features/architecture_check/cli.py](/Users/gorky/Projects/agentic/src/agentic/features/architecture_check/cli.py)

## Boundary

This page is for explaining the feature, not for embedding rule-routing behavior or code-level internals exhaustively.