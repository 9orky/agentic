from __future__ import annotations

from pathlib import Path


SHARED_RULE_PATHS = (
    Path("AGENT.md"),
    Path("feature") / "FEATURE.md",
    Path("feature") / "layers" / "DOMAIN.md",
    Path("feature") / "layers" / "INFRASTRUCTURE.md",
    Path("feature") / "layers" / "APPLICATION.md",
    Path("feature") / "layers" / "UI.md",
    Path("module") / "MODULE.md",
    Path("planning") / "PLANNING.md",
    Path("planning") / "phases" / "BIG_PICTURE.md",
    Path("planning") / "phases" / "STEPS.md",
    Path("refactoring") / "REFACTORING.md",
    Path("tests") / "TESTS.md",
)
LOCAL_EXTENSION_DIRECTORIES = (
    Path("rules") / "overrides",
    Path("rules") / "project-specific",
)
CONFIG_FILE_NAME = "agentic.yaml"
