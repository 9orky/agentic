from __future__ import annotations

from pathlib import Path

from ...infrastructure import ExtractorRuntime
from ..services.dependency_map_builder import BuildDependencyMapResult, DependencyMapBuildError, DependencyMapBuilder, build_default_dependency_map_builder


class BuildDependencyMapQuery:
    def __init__(self, *, dependency_map_builder: DependencyMapBuilder) -> None:
        self._dependency_map_builder = dependency_map_builder

    def execute(
        self,
        project_root: Path,
        explicit_config_path: str | None = None,
        *,
        extractor_runtime: ExtractorRuntime | None = None,
    ) -> BuildDependencyMapResult:
        return self._dependency_map_builder.build(
            project_root,
            explicit_config_path,
            extractor_runtime=extractor_runtime,
        )


def build_default_build_dependency_map_query() -> BuildDependencyMapQuery:
    return BuildDependencyMapQuery(
        dependency_map_builder=build_default_dependency_map_builder(),
    )


build_dependency_map = build_default_build_dependency_map_query().execute

__all__ = [
    "BuildDependencyMapQuery",
    "BuildDependencyMapResult",
    "DependencyMapBuildError",
    "build_default_build_dependency_map_query",
    "build_dependency_map",
]
