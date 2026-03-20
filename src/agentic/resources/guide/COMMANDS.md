# Commands

Use this document to understand the common `agentic` commands available during a session.

Read this early so you do not guess how to interact with the local `agentic/` contract.

## Common Commands

### `agentic`

Bootstrap the local `agentic/` folder in the current project.

Use this when:

1. the project does not yet have a local `agentic/` folder
2. you want to refresh your understanding of the next LLM handoff step

### `agentic init`

Explicit bootstrap command for the local `agentic/` folder.

Use this when:

1. you want the same behavior as bare `agentic`
2. you want to pass `--project-root` explicitly

Example:

```bash
agentic init --project-root /path/to/project
```

### `agentic --llm`

Print the handoff prompt that explains how the user's LLM should work with the local `agentic/` folder.

Use this when:

1. the local folder exists or has just been bootstrapped
2. the next step is to hand control to an LLM session

### `agentic update`

Refresh the shared `agentic` docs in a project from the installed package.

Use this when:

1. the package version changed and you want the latest shared rules, guide docs, and reference docs
2. you want to add any newly shipped shared files into an existing project-local `agentic/` folder

What it does:

1. refreshes all shared files under `rules/`, `guide/`, and `reference/`
2. preserves `agentic/agentic.yaml`
3. preserves repo-local files under `rules/project-specific/`

Example:

```bash
agentic update
agentic update --project-root /path/to/project
```

### `agentic check`

Run the architecture checker against the current project.

Use this when:

1. you changed code and want to verify the configured boundaries still hold
2. you changed `agentic/agentic.yaml` and want to test the new rule set

Examples:

```bash
agentic check
agentic check --project-root /path/to/project
agentic check --config /path/to/agentic.yaml
```

### `agentic help`

Print the command summary and available options.

Use this when:

1. you need the CLI entry points quickly
2. you want the tool to enumerate the supported command surface instead of inferring it

### `agentic --help`

Print the full argparse help output.

Use this when:

1. you need detailed CLI flags
2. you want the canonical parser output

## Verification Default

After code updates, the default architecture verification command is:

```bash
agentic check
```

After updating shared docs from the package, the default follow-up command is:

```bash
agentic check
```