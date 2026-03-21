from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from ...domain.value_object import CheckerError
from ...infrastructure import ExtractorRuntime
from ..queries.describe_architecture import DescribeArchitectureQuery
from ..services.runtime_registry import ExtractorRuntimeFactory


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
        describe_architecture_query: DescribeArchitectureQuery | None = None,
        extractor_runtime_factory: ExtractorRuntimeFactory | None = None,
    ) -> None:
        self._describe_architecture_query = describe_architecture_query or DescribeArchitectureQuery()
        self._extractor_runtime_factory = extractor_runtime_factory or ExtractorRuntimeFactory()

    def run(
        self,
        project_root: Path,
        explicit_config_path: str | None = None,
        *,
        extractor_runtime: ExtractorRuntime | None = None,
    ) -> CheckResult:
        runtime = extractor_runtime or self._extractor_runtime_factory.create()

        summary = self._describe_architecture_query.describe(
            project_root,
            explicit_config_path,
            extractor_runtime=runtime,
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


run_architecture_check = RunArchitectureCheckCommand().run

__all__ = ["CheckResult", "RunArchitectureCheckCommand",
           "run_architecture_check"]
