# Workflow

Use this document for the operational side of agentic.

The local `agentic/` folder is the durable communication boundary between the user and the user's LLM.

Treat the folder like this:

1. `agentic/rules/` contains coding and planning rules
2. `agentic/guide/` contains operational guidance for using agentic during a session
3. `agentic/reference/` contains technical reference material the checker and LLMs share
4. `agentic/agentic.yaml` is the user-editable architecture agreement

Do not use `agentic/` as a scratchpad for temporary plans, execution logs, or one-off notes.

## Session Reading Order

At the start of a session, read in this order:

1. the project's task manifest, task runner config, or documented command entry point
2. `guide/WORKFLOW.md`
3. `guide/COMMANDS.md`
4. `rules/AGENT.md`
5. `reference/ARCHITECTURE_MAP.md` when architecture rules or checker behavior matter
6. `rules/project-specific/` when repo-local clarifications exist

## Project-Specific Guidance

Use `rules/project-specific/` as a curated extension layer.

That means:

1. add a new file only when the clarification has its own stable topic
2. update an existing file when the clarification belongs to an established topic
3. name files by the durable project concern, not by the current task or ticket
4. do not dump prompt transcripts, scratch notes, or temporary plans into this folder
5. keep each file short enough that future LLM runs can actually reuse it

## Shared Rails Versus Local Clarifications

1. keep shared rule files under `rules/` stable unless the package itself is being improved
2. place repo-specific clarifications under `rules/project-specific/`
3. if a shared rule is wrong for many repos, treat that as an upstream package issue rather than hiding the problem in one local clarification

When the installed package ships new shared docs, use `agentic update` inside the target project and then run `agentic check`.