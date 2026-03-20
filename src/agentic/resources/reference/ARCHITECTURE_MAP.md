# Architecture Map

Use this document to understand the extracted project facts that `agentic check` and architecture-aware LLM work rely on.

The architecture map is the common schema produced by per-language extractor scripts.

Its purpose is to give the checker and the user's LLM one shared view of the repository structure without hard-coding language-specific parsing into the rule engine.

## Contract

Each extractor must return one JSON object.

Each key is a repo-relative file path.

Each value must contain all of these fields:

- `imports`: list of imported module or path references
- `classes`: list of class names declared in the file
- `functions`: list of function names declared in the file

Example shape:

```json
{
  "src/domain/logic.py": {
    "imports": ["src.infra.database"],
    "classes": ["LogicService"],
    "functions": ["build_logic"]
  }
}
```

## Normalization Rules

1. file paths are repo-relative and normalized to forward slashes
2. empty path keys are invalid
3. `imports`, `classes`, and `functions` must all be present
4. those fields must contain only strings
5. empty strings are discarded during normalization

The checker validates this contract before evaluating any rules.

## What The Checker Uses

Today the checker uses the architecture map mainly for dependency boundaries.

That means:

1. `imports` directly affect boundary evaluation
2. `classes` and `functions` are part of the shared schema even when a particular rule does not yet consume them
3. future rules may safely build on this schema as long as the contract changes explicitly

## Limits

The architecture map is a practical extraction layer, not a perfect semantic model.

You should assume:

1. extractor quality depends on language support and parser strategy
2. an extractor may intentionally model only the data needed for architectural reasoning
3. if a repo needs richer facts, the contract should be extended deliberately rather than inferred ad hoc inside prompts

## Shared Rails And Local Clarifications

If this schema is correct but a repo needs additional local interpretation, document that in `rules/project-specific/`.

If the schema itself is missing an important shared concept, treat that as a package improvement rather than hiding a workaround in one repo.