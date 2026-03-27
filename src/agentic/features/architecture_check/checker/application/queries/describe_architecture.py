from __future__ import annotations

from pathlib import Path

from ...infrastructure import ExtractorRuntime
from ..services.architecture_summary_service import ArchitectureSummaryService
from ..services.architecture_summary_service import build_default_architecture_summary_service
from .architecture_summary import ArchitectureSummary


class DescribeArchitectureQuery:
    def __init__(
        self,
        *,
        summary_service: ArchitectureSummaryService,
    ) -> None:
        self._summary_service = summary_service

    def describe(
        self,
        project_root: Path,
        explicit_config_path: str | None = None,
        *,
        extractor_runtime: ExtractorRuntime | None = None,
    ) -> ArchitectureSummary:
        return self._summary_service.describe(
            project_root,
            explicit_config_path,
            extractor_runtime=extractor_runtime,
        )


def build_default_describe_architecture_query() -> DescribeArchitectureQuery:
    return DescribeArchitectureQuery(
        summary_service=build_default_architecture_summary_service(),
    )


describe_architecture = build_default_describe_architecture_query().describe

__all__ = ["ArchitectureSummary",
           "DescribeArchitectureQuery", "describe_architecture"]
