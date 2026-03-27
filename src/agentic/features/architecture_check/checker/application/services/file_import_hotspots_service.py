from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from ...domain import ArchitectureCheckConfigError, CheckerError
from ...infrastructure import ExtractorRuntime, ExtractorRuntimeFactory, ExtractorSpecRegistry
from .architecture_report_builder.dependency_graph_builder import DependencyGraphBuilder
from .config_load_service import ConfigLoadService, build_default_config_load_service

FileImportHotspotsSortBy = Literal["imports_count", "imported_by_count"]


@dataclass(frozen=True)
class FileImportHotspotEntry:
    path: str
    imports_count: int
    imported_by_count: int


@dataclass(frozen=True)
class FileImportHotspotsResult:
    entries: tuple[FileImportHotspotEntry, ...]
    sort_by: FileImportHotspotsSortBy
    descending: bool

    def to_json_dict(self) -> dict[str, object]:
        return {
            "entries": [
                {
                    "path": entry.path,
                    "imports_count": entry.imports_count,
                    "imported_by_count": entry.imported_by_count,
                }
                for entry in self.entries
            ],
            "sort_by": self.sort_by,
            "descending": self.descending,
        }


class FileImportHotspotsService:
    def __init__(
        self,
        *,
        config_load_service: ConfigLoadService,
        extractor_runtime_factory: ExtractorRuntimeFactory,
        extractor_spec_registry: ExtractorSpecRegistry,
        dependency_graph_builder: DependencyGraphBuilder,
    ) -> None:
        self._config_load_service = config_load_service
        self._extractor_runtime_factory = extractor_runtime_factory
        self._extractor_spec_registry = extractor_spec_registry
        self._dependency_graph_builder = dependency_graph_builder

    def describe(
        self,
        project_root: Path,
        explicit_config_path: str | None = None,
        *,
        sort_by: FileImportHotspotsSortBy = "imported_by_count",
        descending: bool = True,
        extractor_runtime: ExtractorRuntime | None = None,
    ) -> FileImportHotspotsResult:
        try:
            load_result = self._config_load_service.load(
                project_root,
                explicit_config_path,
            )
        except ArchitectureCheckConfigError as exc:
            raise CheckerError(str(exc)) from exc

        runtime = extractor_runtime or self._extractor_runtime_factory.create()
        extractor_spec = self._extractor_spec_registry.get(
            load_result.config.language)
        extraction_result = runtime.run(
            extractor_spec,
            project_root,
            load_result.config.exclusions,
        )
        graph = self._dependency_graph_builder.build(extraction_result.files)
        tracked_files = set(extraction_result.files.keys())

        imports_by_file = {file_path: set() for file_path in tracked_files}
        imported_by_file = {file_path: set() for file_path in tracked_files}

        for edge in graph.edges:
            if edge.from_id not in tracked_files or edge.to_id not in tracked_files:
                continue
            imports_by_file[edge.from_id].add(edge.to_id)
            imported_by_file[edge.to_id].add(edge.from_id)

        entries = tuple(
            sorted(
                (
                    FileImportHotspotEntry(
                        path=file_path,
                        imports_count=len(imports_by_file[file_path]),
                        imported_by_count=len(imported_by_file[file_path]),
                    )
                    for file_path in tracked_files
                ),
                key=lambda entry: self._sort_key(entry, sort_by, descending),
            )
        )

        return FileImportHotspotsResult(
            entries=entries,
            sort_by=sort_by,
            descending=descending,
        )

    @staticmethod
    def _sort_key(
        entry: FileImportHotspotEntry,
        sort_by: FileImportHotspotsSortBy,
        descending: bool,
    ) -> tuple[int, int, str]:
        if sort_by == "imports_count":
            primary_value = entry.imports_count
            secondary_value = entry.imported_by_count
        else:
            primary_value = entry.imported_by_count
            secondary_value = entry.imports_count

        if descending:
            return (-primary_value, -secondary_value, entry.path)
        return (primary_value, secondary_value, entry.path)


def build_default_file_import_hotspots_service() -> FileImportHotspotsService:
    return FileImportHotspotsService(
        config_load_service=build_default_config_load_service(),
        extractor_runtime_factory=ExtractorRuntimeFactory(),
        extractor_spec_registry=ExtractorSpecRegistry(),
        dependency_graph_builder=DependencyGraphBuilder(),
    )


__all__ = [
    "FileImportHotspotEntry",
    "FileImportHotspotsResult",
    "FileImportHotspotsService",
    "FileImportHotspotsSortBy",
    "build_default_file_import_hotspots_service",
]
