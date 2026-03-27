from __future__ import annotations

from pathlib import Path

from ...domain import ArchitectureCheckConfigError, CheckerError
from ...infrastructure import ExtractorRuntime
from ..queries import ArchitectureSummary
from .architecture_report_builder import ArchitectureReportBuilder, ViolationRenderer
from .architecture_report_builder import build_default_architecture_report_builder


class ArchitectureSummaryService:
    def __init__(
        self,
        *,
        report_builder: ArchitectureReportBuilder,
        violation_renderer: ViolationRenderer,
    ) -> None:
        self._report_builder = report_builder
        self._violation_renderer = violation_renderer

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


def build_default_architecture_summary_service() -> ArchitectureSummaryService:
    return ArchitectureSummaryService(
        report_builder=build_default_architecture_report_builder(),
        violation_renderer=ViolationRenderer(),
    )


__all__ = ["ArchitectureSummaryService"]
