# Architecture Rule Checker

This repository acts as an intelligent, zero-dependency "drop-in brain" meant for both humans and AI agents (like GitHub Copilot) to enforce architectural boundaries via strict codebase parsing.

## Folder Structure

```text
my-project/
├── agentic/                      <-- This repository (the drop-in brain)
│   ├── arch/                     <-- The test engine & extractors
│   ├── rules/                    <-- Static, read-only architectural rules
│   │   ├── example-rule.md     
│   │   └── project-specific/     <-- Custom instructions for this project (Gitignored except .gitkeep)
│   ├── arch-config.json          <-- Standardized JSON config for the engine (has simple example, project rules must be configured here)
│   └── README.md                 <-- Core instructions (you are here)
└── src/                          <-- Your actual application code
```

## How to Configure (`agentic/arch-config.json`)

The engine reads technical parsing boundaries from `agentic/arch-config.json`. This file contains a basic example to get you started - you must configure it with your own project rules and boundaries. Note that the `rules/project-specific` folder is gitignored (except for `.gitkeep`), meaning you can store ephemeral custom rules or configurations there.

**Example `agentic/arch-config.json`:**
```json
{
  "language": "python",
  "exclusions": [
    "tests/",
    "node_modules/"
  ],
  "rules": {
    "boundaries": [
      {
        "source": "src/domain",
        "disallow": ["src/infra", "src/ui"]
      }
    ]
  }
}
```
*(Supported languages: `python`, `typescript`, `php`)*

## 🚨 Guidelines for AI Agents

To ensure the integrity of the architecture engine, the following constraints strictly apply:
1. **`rules/` is READ-ONLY:** Agents **must never** rename, edit, or touch the contents of this folder once populated. Exception: The `rules/project-specific/` folder is explicitly meant for custom instructions.
2. **`arch-config.json` is for Boundaries:** This file must be configured with your actual architectural rules and boundaries.
3. **No Artifact Dumping:** None of the above folders are a place to put active session docs, task checklists, or execution plans.
4. **Reporting Issues:** If you encounter bugs, missing features, or structural issues with the architecture checker itself, create and commit an `ISSUES.md` file next to this `README.md` to document them.

## Running the Tests

**For Agents & Humans:**
From the root of your project, run:
```bash
python3 agentic/arch/run_tests.py
```

The runner will look for `arch-config.json` in these locations, in order:

1. `--config <path>` if provided
2. `<project-root>/arch-config.json`
3. `<project-root>/agentic/arch-config.json`
4. Next to the `agentic/arch` folder

If boundaries are breached, the script will output a clear list of violations:
```text
[VIOLATION] src/domain/Logic.py
  -> Layer 'src/domain' cannot depend on 'src/infra'
  -> Offending import: 'src/infra/Database'
```
*Note: A capable AI should use this output to autonomously correct the offending code and re-run the tests until the output is clean.*
