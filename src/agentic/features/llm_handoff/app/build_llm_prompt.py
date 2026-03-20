from __future__ import annotations

from pathlib import Path


def build_llm_prompt(project_root: Path) -> str:
    agentic_dir = project_root / "agentic"
    return f"""You are working in a project that uses agentic as the communication boundary between the user and their LLM.

Your job:
1. Start by reading agentic/guide/WORKFLOW.md.
2. Read agentic/guide/COMMANDS.md so you know the common commands available during the session.
3. Read agentic/rules/AGENT.md for the coding and planning rule set.
4. Read agentic/reference/ARCHITECTURE_MAP.md before changing architecture rules or check behavior.
5. Treat the local {agentic_dir.name}/ directory as the project SSOT for rules, architecture decisions, and future agent handoff.
6. Treat shared rule files under agentic/rules/ as stable coding rails. Put repo-specific clarifications only under agentic/rules/project-specific/.
7. Inspect the repository structure, package manager files, task runner config, and documented commands before proposing changes.
8. Review agentic/agentic.yaml as the user-editable agreement for language, exclusions, and dependency boundaries.
9. Identify project-specific conventions, ownership boundaries, naming rules, and allowed dependency directions.
10. Write project-specific guidance into agentic/rules/project-specific/ so future LLM runs inherit it instead of rediscovering it.
11. If the shared rules and the project reality conflict, keep the shared rails intact, record the repo-specific clarification locally, and clearly note when the shared package should be improved upstream.
12. Tell the user what future prompt they should use so agentic/ stays the first place every LLM run reads.

Your output requirements:
- Be concrete and repo-specific.
- Ask the user for missing architecture decisions instead of guessing.
- Prefer the smallest set of project-specific documents needed to make future runs consistent.
- Keep the agentic/ folder clean: no task scratchpads, no temporary execution logs, no unrelated artifacts.
- Do not treat agentic/ as a one-session scratchpad. Treat it as a durable collaboration surface the next LLM run must understand.
"""
