from __future__ import annotations

from pathlib import Path


CORE_RULE_DOCUMENTS = (
    "AGENT.md",
    "FEATURE.md",
    "FEATURE_LAYOUT.md",
    "MODULE.md",
    "PLANNING.md",
    "REFACTORING.md",
    "TESTS.md",
)
LOCAL_EXTENSION_DIRECTORIES = (
    Path("rules") / "overrides",
    Path("rules") / "project-specific",
)
CONFIG_FILE_NAME = "agentic.yaml"
