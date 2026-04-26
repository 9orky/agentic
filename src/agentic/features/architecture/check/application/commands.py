from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from ...map.infrastructure import ExtractorRuntime
from ..domain import CheckerError
from .queries import DescribeArchitectureQuery, build_default_describe_architecture_query


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
        describe_architecture_query: DescribeArchitectureQuery,
    ) -> None:
        self._describe_architecture_query = describe_architecture_query

    def run(
        self,
        project_root: Path,
        explicit_config_path: str | None = None,
        *,
        extractor_runtime: ExtractorRuntime | None = None,
    ) -> CheckResult:
        summary = self._describe_architecture_query.describe(
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
        describe_architecture_query=build_default_describe_architecture_query(),
    )


run_architecture_check = build_default_run_architecture_check_command().run

__all__ = ["CheckResult", "RunArchitectureCheckCommand", "run_architecture_check"]
