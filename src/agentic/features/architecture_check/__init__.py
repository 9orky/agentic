from __future__ import annotations

from pathlib import Path

from .adapters.subprocess_runtime import SubprocessExtractorRuntime
from .app.run_architecture_check import run_architecture_check as _run_architecture_check
from .contracts import CheckResult, CheckerError

__all__ = ["run_architecture_check", "CheckResult", "CheckerError"]


def run_architecture_check(project_root: Path, explicit_config_path: str | None = None) -> CheckResult:
    return _run_architecture_check(
        project_root,
        explicit_config_path,
        extractor_runtime=SubprocessExtractorRuntime(),
    )
