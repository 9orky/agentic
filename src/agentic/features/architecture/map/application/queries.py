from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from ..domain import (
    ArchitectureConfig,
    ArchitectureConfigError,
    CheckerError,
    ConfigLoadResult,
    DependencyGraph,
    DependencyGraphBuilder,
    ExtractionResult,
)
from ..infrastructure import (
    ExtractorRuntime,
    ExtractorSpecRegistry,
    config_loader,
    extractor_registry,
    extractor_runtime_factory,
)
from ..infrastructure.config_loader import ConfigLoader
from ..infrastructure.extractor_runtime import ExtractorRuntimeFactory


class LoadArchitectureConfigQuery:
    def __init__(self, *, config_loader: ConfigLoader) -> None:
        self._config_loader = config_loader

    def load(
        self,
        project_root: Path,
        explicit_config_path: str | None = None,
    ) -> ConfigLoadResult:
        config_path = self._config_loader.resolve_path(project_root, explicit_config_path)
        if config_path is None:
            raise ArchitectureConfigError(
                "Could not find a configuration file. "
                f"Looked for an explicit path, {self._config_loader.config_search_description()}."
            )

        raw_text = self._config_loader.read_text(config_path)
        raw_data, source_format = self._config_loader.load_mapping(raw_text, config_path)
        config = ArchitectureConfig.validate_mapping(raw_data, config_path)
        return ConfigLoadResult(path=config_path, config=config, source_format=source_format)


@dataclass(frozen=True)
class BuildDependencyMapResult:
    load_result: ConfigLoadResult
    runtime_command: str
    extraction_result: ExtractionResult
    graph: DependencyGraph


class DependencyMapBuildError(CheckerError):
    def __init__(
        self,
        *,
        load_result: ConfigLoadResult,
        runtime_command: str,
        message: str,
    ) -> None:
        super().__init__(message)
        self.load_result = load_result
        self.runtime_command = runtime_command


class BuildDependencyMapQuery:
    def __init__(
        self,
        *,
        load_architecture_config_query: LoadArchitectureConfigQuery,
        extractor_spec_registry: ExtractorSpecRegistry,
        extractor_runtime_factory: ExtractorRuntimeFactory,
        dependency_graph_builder: DependencyGraphBuilder,
    ) -> None:
        self._load_architecture_config_query = load_architecture_config_query
        self._extractor_spec_registry = extractor_spec_registry
        self._extractor_runtime_factory = extractor_runtime_factory
        self._dependency_graph_builder = dependency_graph_builder

    def execute(
        self,
        project_root: Path,
        explicit_config_path: str | None = None,
        *,
        extractor_runtime: ExtractorRuntime | None = None,
    ) -> BuildDependencyMapResult:
        load_result = self._load_architecture_config_query.load(project_root, explicit_config_path)
        extractor_spec = self._extractor_spec_registry.get(load_result.config.language)
        runtime_command = extractor_spec.command
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
            graph=self._dependency_graph_builder.build(extraction_result.files),
        )


def build_default_load_architecture_config_query() -> LoadArchitectureConfigQuery:
    return LoadArchitectureConfigQuery(config_loader=config_loader)


def build_default_build_dependency_map_query() -> BuildDependencyMapQuery:
    return BuildDependencyMapQuery(
        load_architecture_config_query=build_default_load_architecture_config_query(),
        extractor_spec_registry=extractor_registry,
        extractor_runtime_factory=extractor_runtime_factory,
        dependency_graph_builder=DependencyGraphBuilder(),
    )


load_architecture_config = build_default_load_architecture_config_query().load
build_dependency_map = build_default_build_dependency_map_query().execute

__all__ = [
    "BuildDependencyMapQuery",
    "BuildDependencyMapResult",
    "DependencyMapBuildError",
    "LoadArchitectureConfigQuery",
    "build_dependency_map",
    "load_architecture_config",
]
