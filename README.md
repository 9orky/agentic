# Architecture Rule Checker

This repository acts as an intelligent, zero-dependency "drop-in brain" meant for both humans and AI agents (like GitHub Copilot) to enforce architectural boundaries via strict codebase parsing.

## Folder Structure

```text
my-project/
├── agentic/                      <-- This repository (the drop-in brain)
│   ├── arch/                     <-- The test engine & extractors
│   ├── project-specific/         <-- Custom instructions for this project (Gitignored except .gitkeep)
│   │   └── arch-config.json      <-- Standardized JSON config for the engine
│   ├── rules/                    <-- Static, read-only architectural rules
│   │   └── example-rule.md     
│   └── README.md                 <-- Core instructions (you are here)
└── src/                          <-- Your actual application code
```

## How to Configure (`agentic/project-specific/arch-config.json`)

The engine reads technical parsing boundaries from `agentic/project-specific/arch-config.json`. Note that the `project-specific` folder is gitignored (except for `.gitkeep`), meaning these configs are ephemeral or maintained by individual developers/agents locally.

**Example `agentic/project-specific/arch-config.json`:**
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
1. **`rules/` is READ-ONLY:** Agents **must never** rename, edit, or touch the contents of this folder once populated.
2. **`project-specific/` is for Custom Configs:** Used strictly for instructions and JSON config overrides tailored to the local environment.
3. **No Artifact Dumping:** None of the above folders are a place to put active session docs, task checklists, or execution plans.

## Running the Tests

**For Agents & Humans:**
From the root of your project, run:
```bash
python3 agentic/arch/run_tests.py
```

If boundaries are breached, the script will output a clear list of violations:
```text
[VIOLATION] src/domain/Logic.py
  -> Layer 'src/domain' cannot depend on 'src/infra'
  -> Offending import: 'src/infra/Database'
```
*Note: A capable AI should use this output to autonomously correct the offending code and re-run the tests until the output is clean.*
