from __future__ import annotations

from pathlib import Path

from ...infrastructure import ExtractorRuntime
from ..services.architecture_report_builder import ArchitectureCheckReport, ArchitectureReportBuilder, ViolationGroup
from ..services.architecture_report_builder.service import build_default_architecture_report_builder


class BuildArchitectureReportQuery:
    def __init__(
        self,
        *,
        report_builder: ArchitectureReportBuilder,
    ) -> None:
        self._report_builder = report_builder

    def execute(
        self,
        project_root: Path,
        explicit_config_path: str | None = None,
        *,
        extractor_runtime: ExtractorRuntime | None = None,
    ) -> ArchitectureCheckReport:
        return self._report_builder.build(
            project_root,
            explicit_config_path,
            extractor_runtime=extractor_runtime,
        )

    def build_dot_report(self, report: ArchitectureCheckReport) -> str:
        return self._report_builder.build_dot_report(report)

    def build_violation_groups(
        self,
        report: ArchitectureCheckReport,
    ) -> tuple[ViolationGroup, ...]:
        return self._report_builder.build_violation_groups(report)


def build_default_architecture_report_query() -> BuildArchitectureReportQuery:
    return BuildArchitectureReportQuery(
        report_builder=build_default_architecture_report_builder(),
    )


__all__ = ["BuildArchitectureReportQuery", "ViolationGroup"]
