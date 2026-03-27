from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from ...domain import CheckerError
from ...infrastructure import ExtractorRuntime
from ..services.architecture_report_builder import ArchitectureCheckReport, ArchitectureReportBuilder
from ..services.architecture_report_builder.service import build_default_architecture_report_builder


@dataclass(frozen=True)
class ViolationGroup:
    title: str
    entries: tuple[str, ...]


@dataclass(frozen=True)
class BuildArchitectureReportResult:
    report: ArchitectureCheckReport
    dot_report: str
    violation_groups: tuple[ViolationGroup, ...]

    @property
    def check_error(self) -> str | None:
        return self.report.check_error

    @property
    def violations(self):
        return self.report.violations

    @property
    def files_found(self) -> int:
        return self.report.files_found

    @property
    def files_excluded(self) -> int:
        return self.report.files_excluded

    @property
    def files_checked(self) -> int:
        return self.report.files_checked

    def to_json_dict(self) -> dict[str, object]:
        return self.report.to_json_dict()


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
    ) -> BuildArchitectureReportResult:
        artifacts = self._report_builder.build_artifacts(
            project_root,
            explicit_config_path,
            extractor_runtime=extractor_runtime,
        )
        return BuildArchitectureReportResult(
            report=artifacts.report,
            dot_report=artifacts.dot_report,
            violation_groups=tuple(
                ViolationGroup(title=title, entries=entries)
                for title, entries in artifacts.violation_groups
            ),
        )


def build_default_architecture_report_query() -> BuildArchitectureReportQuery:
    return BuildArchitectureReportQuery(
        report_builder=build_default_architecture_report_builder(),
    )


__all__ = ["BuildArchitectureReportQuery", "CheckerError", "ViolationGroup"]
