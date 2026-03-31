from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from ...domain import CheckerError, ConfigLoadResult, DependencyGraph, ExtractedFile, ExtractionResult
from ...infrastructure import ExtractorRuntime, ExtractorRuntimeFactory, ExtractorSpecRegistry
from .config_load_service import ConfigLoadService, build_default_config_load_service


class DependencyGraphBuilder:
    def build(self, architecture_map: dict[str, ExtractedFile]) -> DependencyGraph:
        from ...domain import NodeSelector

        graph = DependencyGraph()

        for file_path, extracted_file in architecture_map.items():
            graph.add_node(file_path)
            for imported_reference in extracted_file.imports:
                normalized_import = NodeSelector.normalize_import_reference(
                    imported_reference)
                if not normalized_import:
                    continue
                graph.add_edge(file_path, normalized_import)

        return graph


@dataclass(frozen=True)
class BuildDependencyMapResult:
    load_result: ConfigLoadResult
    runtime_command: str
    extraction_result: ExtractionResult
    graph: DependencyGraph


class DependencyMapBuildError(CheckerError):
    def __init__(self, *, load_result: ConfigLoadResult, runtime_command: str, message: str) -> None:
        super().__init__(message)
        self.load_result = load_result
        self.runtime_command = runtime_command


class DependencyMapBuilder:
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

    def build(
        self,
        project_root: Path,
        explicit_config_path: str | None = None,
        *,
        extractor_runtime: ExtractorRuntime | None = None,
    ) -> BuildDependencyMapResult:
        load_result = self._config_load_service.load(
            project_root, explicit_config_path)
        extractor_spec = self._extractor_spec_registry.get(
            load_result.config.language)
        runtime_command = getattr(extractor_spec, "command", "")
        runtime = extractor_runtime or self._extractor_runtime_factory.create()

        try:
            extraction_result = runtime.run(
                extractor_spec,
                project_root,
                load_result.config.exclusions,
            )
        except CheckerError as exc:
            raise DependencyMapBuildError(
                load_result=load_result,
                runtime_command=runtime_command,
                message=str(exc),
            ) from exc

        return BuildDependencyMapResult(
            load_result=load_result,
            runtime_command=runtime_command,
            extraction_result=extraction_result,
            graph=self._dependency_graph_builder.build(
                extraction_result.files),
        )


def build_default_dependency_map_builder() -> DependencyMapBuilder:
    return DependencyMapBuilder(
        config_load_service=build_default_config_load_service(),
        extractor_runtime_factory=ExtractorRuntimeFactory(),
        extractor_spec_registry=ExtractorSpecRegistry(),
        dependency_graph_builder=DependencyGraphBuilder(),
    )


__all__ = [
    "BuildDependencyMapResult",
    "DependencyGraphBuilder",
    "DependencyMapBuildError",
    "DependencyMapBuilder",
    "build_default_dependency_map_builder",
]
