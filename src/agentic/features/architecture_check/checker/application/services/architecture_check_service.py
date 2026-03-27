from __future__ import annotations

from pathlib import Path

from ...infrastructure import ExtractorRuntime, ExtractorRuntimeFactory
from .architecture_summary_service import ArchitectureSummary
from .architecture_summary_service import ArchitectureSummaryService
from .architecture_summary_service import build_default_architecture_summary_service


class ArchitectureCheckService:
    def __init__(
        self,
        *,
        summary_service: ArchitectureSummaryService,
        extractor_runtime_factory: ExtractorRuntimeFactory,
    ) -> None:
        self._summary_service = summary_service
        self._extractor_runtime_factory = extractor_runtime_factory

    def check(
        self,
        project_root: Path,
        explicit_config_path: str | None = None,
        *,
        extractor_runtime: ExtractorRuntime | None = None,
    ) -> ArchitectureSummary:
        runtime = extractor_runtime or self._extractor_runtime_factory.create()
        return self._summary_service.describe(
            project_root,
            explicit_config_path,
            extractor_runtime=runtime,
        )


def build_default_architecture_check_service() -> ArchitectureCheckService:
    return ArchitectureCheckService(
        summary_service=build_default_architecture_summary_service(),
        extractor_runtime_factory=ExtractorRuntimeFactory(),
    )


__all__ = ["ArchitectureCheckService"]
