from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from ...domain import CheckerError
from ...infrastructure import ExtractorRuntime
from ..services.architecture_check_service import ArchitectureCheckService
from ..services.architecture_check_service import build_default_architecture_check_service


@dataclass(frozen=True)
class CheckResult:
    project_root: Path
    config_path: Path
    config_format: str
    files_found: int
    files_excluded: int
    files_checked: int
    violations: list[str]


class RunArchitectureCheckCommand:
    def __init__(
        self,
        *,
        check_service: ArchitectureCheckService,
    ) -> None:
        self._check_service = check_service

    def run(
        self,
        project_root: Path,
        explicit_config_path: str | None = None,
        *,
        extractor_runtime: ExtractorRuntime | None = None,
    ) -> CheckResult:
        summary = self._check_service.check(
            project_root,
            explicit_config_path,
            extractor_runtime=extractor_runtime,
        )
        if summary.check_error is not None:
            raise CheckerError(summary.check_error)

        return CheckResult(
            project_root=summary.project_root,
            config_path=summary.config_path,
            config_format=summary.config_format,
            files_found=summary.files_found,
            files_excluded=summary.files_excluded,
            files_checked=summary.files_checked,
            violations=list(summary.violations),
        )


def build_default_run_architecture_check_command() -> RunArchitectureCheckCommand:
    return RunArchitectureCheckCommand(
        check_service=build_default_architecture_check_service(),
    )


run_architecture_check = build_default_run_architecture_check_command().run

__all__ = ["CheckResult", "RunArchitectureCheckCommand",
           "run_architecture_check"]
