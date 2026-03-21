from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from ...domain.value_object import ArchitectureCheckConfigError, CheckerError
from ...infrastructure import ExtractorRuntime
from ..services.report_builder import ArchitectureReportBuilder
from ..services.violation_renderer import ViolationRenderer


@dataclass(frozen=True)
class ArchitectureSummary:
    project_root: Path
    config_path: Path
    config_format: str
    language: str
    runtime_command: str
    files_found: int = 0
    files_excluded: int = 0
    files_checked: int = 0
    violations: tuple[str, ...] = ()
    check_error: str | None = None


class DescribeArchitectureQuery:
    def __init__(
        self,
        report_builder: ArchitectureReportBuilder | None = None,
        violation_renderer: ViolationRenderer | None = None,
    ) -> None:
        self._report_builder = report_builder or ArchitectureReportBuilder()
        self._violation_renderer = violation_renderer or ViolationRenderer()

    def describe(
        self,
        project_root: Path,
        explicit_config_path: str | None = None,
        *,
        extractor_runtime: ExtractorRuntime | None = None,
    ) -> ArchitectureSummary:
        try:
            report = self._report_builder.build(
                project_root,
                explicit_config_path,
                extractor_runtime=extractor_runtime,
            )
        except ArchitectureCheckConfigError as exc:
            raise CheckerError(str(exc)) from exc

        return ArchitectureSummary(
            project_root=report.project_root,
            config_path=report.config_path,
            config_format=report.config_format,
            language=report.language,
            runtime_command=report.runtime_command,
            files_found=report.files_found,
            files_excluded=report.files_excluded,
            files_checked=report.files_checked,
            violations=tuple(
                self._violation_renderer.render(violation)
                for violation in report.violations
            ),
            check_error=report.check_error,
        )


describe_architecture = DescribeArchitectureQuery().describe

__all__ = ["ArchitectureSummary",
           "DescribeArchitectureQuery", "describe_architecture"]
