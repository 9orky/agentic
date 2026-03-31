from __future__ import annotations

from pathlib import Path
from typing import Protocol

from ....dependency_map.infrastructure import ExtractorRuntime
from ..services.file_import_hotspots_service import FileImportHotspotEntry, FileImportHotspotsResult, FileImportHotspotsSortBy


class FileImportHotspotsServiceLike(Protocol):
    def describe(
        self,
        project_root: Path,
        explicit_config_path: str | None = None,
        *,
        sort_by: FileImportHotspotsSortBy = "imported_by_count",
        descending: bool = True,
        extractor_runtime: ExtractorRuntime | None = None,
    ) -> FileImportHotspotsResult:
        ...


class DescribeFileImportHotspotsQuery:
    def __init__(
        self,
        *,
        file_import_hotspots_service: FileImportHotspotsServiceLike,
    ) -> None:
        self._file_import_hotspots_service = file_import_hotspots_service

    def describe(
        self,
        project_root: Path,
        explicit_config_path: str | None = None,
        *,
        sort_by: FileImportHotspotsSortBy = "imported_by_count",
        descending: bool = True,
        extractor_runtime: ExtractorRuntime | None = None,
    ) -> FileImportHotspotsResult:
        return self._file_import_hotspots_service.describe(
            project_root,
            explicit_config_path,
            sort_by=sort_by,
            descending=descending,
            extractor_runtime=extractor_runtime,
        )


def build_default_describe_file_import_hotspots_query() -> DescribeFileImportHotspotsQuery:
    from ..services.file_import_hotspots_service import build_default_file_import_hotspots_service

    return DescribeFileImportHotspotsQuery(
        file_import_hotspots_service=build_default_file_import_hotspots_service(),
    )


__all__ = [
    "DescribeFileImportHotspotsQuery",
    "FileImportHotspotEntry",
    "FileImportHotspotsResult",
    "build_default_describe_file_import_hotspots_query",
]