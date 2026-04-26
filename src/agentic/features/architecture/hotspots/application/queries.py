from __future__ import annotations

from pathlib import Path

from ...map.application import (
    BuildDependencyMapQuery,
    DependencyMapBuildError,
    build_default_build_dependency_map_query,
)
from ...map.application.metrics import (
    FileArchitectureMetrics,
    derive_file_architecture_metrics,
)
from ...map.domain import ArchitectureConfigError, CheckerError
from ...map.infrastructure import ExtractorRuntime
from ..domain import (
    FileImportHotspotEntry,
    FileImportHotspotsResult,
    FileImportHotspotsSortBy,
    HotspotExplanation,
    HotspotScore,
    HotspotSignal,
    SemanticHotspotReport,
)


class DescribeFileImportHotspotsQuery:
    def __init__(
        self,
        *,
        build_dependency_map_query: BuildDependencyMapQuery,
    ) -> None:
        self._build_dependency_map_query = build_dependency_map_query

    def describe(
        self,
        project_root: Path,
        explicit_config_path: str | None = None,
        *,
        sort_by: FileImportHotspotsSortBy = "risk_score",
        descending: bool = True,
        top: int | None = None,
        extractor_runtime: ExtractorRuntime | None = None,
    ) -> FileImportHotspotsResult:
        file_metrics = self._derive_metrics(
            project_root,
            explicit_config_path,
            extractor_runtime=extractor_runtime,
        )
        entries = tuple(
            FileImportHotspotEntry(
                path=metric.path,
                imports_count=metric.imports_count,
                imported_by_count=metric.imported_by_count,
                symbol_count=metric.symbol_count,
                public_symbol_count=metric.public_symbol_count,
                line_count=metric.line_count,
                risk_score=metric.risk_score,
                dominant_signals=metric.dominant_signals,
            )
            for metric in sorted(
                file_metrics,
                key=lambda item: self._sort_key(item, sort_by, descending),
            )[:top]
        )
        return FileImportHotspotsResult(
            entries=entries,
            sort_by=sort_by,
            descending=descending,
        )

    def _derive_metrics(
        self,
        project_root: Path,
        explicit_config_path: str | None,
        *,
        extractor_runtime: ExtractorRuntime | None = None,
    ) -> tuple[FileArchitectureMetrics, ...]:
        try:
            dependency_map_result = self._build_dependency_map_query.execute(
                project_root,
                explicit_config_path,
                extractor_runtime=extractor_runtime,
            )
        except ArchitectureConfigError as exc:
            raise CheckerError(str(exc)) from exc
        except DependencyMapBuildError as exc:
            raise CheckerError(str(exc)) from exc
        return derive_file_architecture_metrics(dependency_map_result)

    @staticmethod
    def _sort_key(
        entry: FileArchitectureMetrics,
        sort_by: FileImportHotspotsSortBy,
        descending: bool,
    ) -> tuple[float, float, str]:
        values = {
            "risk_score": entry.risk_score,
            "imports_count": float(entry.imports_count),
            "imported_by_count": float(entry.imported_by_count),
            "symbol_count": float(entry.symbol_count),
            "public_symbol_count": float(entry.public_symbol_count),
            "line_count": float(entry.line_count),
        }
        primary_value = values[sort_by]
        secondary_value = entry.risk_score if sort_by != "risk_score" else float(entry.imported_by_count)
        if descending:
            return (-primary_value, -secondary_value, entry.path)
        return (primary_value, secondary_value, entry.path)


class ExplainHotspotQuery:
    def __init__(
        self,
        *,
        build_dependency_map_query: BuildDependencyMapQuery,
    ) -> None:
        self._build_dependency_map_query = build_dependency_map_query

    def explain(
        self,
        project_root: Path,
        target_path: str,
        explicit_config_path: str | None = None,
        *,
        extractor_runtime: ExtractorRuntime | None = None,
    ) -> SemanticHotspotReport:
        normalized_target_path = target_path.replace("\\", "/").strip().strip("/")
        if not normalized_target_path:
            raise CheckerError("Hotspot explanation target path must not be empty.")

        file_metrics = self._derive_metrics(
            project_root,
            explicit_config_path,
            extractor_runtime=extractor_runtime,
        )
        for metric in file_metrics:
            if metric.path != normalized_target_path:
                continue
            signals = self._signals_for(metric)
            return SemanticHotspotReport(
                path=metric.path,
                score=HotspotScore(
                    total=metric.risk_score,
                    signals=signals,
                ),
                explanation=HotspotExplanation(
                    summary=self._summary_for(metric),
                    dominant_signals=metric.dominant_signals,
                ),
            )

        raise CheckerError(
            f"Could not find '{normalized_target_path}' in the tracked architecture graph."
        )

    def _derive_metrics(
        self,
        project_root: Path,
        explicit_config_path: str | None,
        *,
        extractor_runtime: ExtractorRuntime | None = None,
    ) -> tuple[FileArchitectureMetrics, ...]:
        return DescribeFileImportHotspotsQuery(
            build_dependency_map_query=self._build_dependency_map_query,
        )._derive_metrics(
            project_root,
            explicit_config_path,
            extractor_runtime=extractor_runtime,
        )

    @staticmethod
    def _signals_for(metric: FileArchitectureMetrics) -> tuple[HotspotSignal, ...]:
        return tuple(
            HotspotSignal(
                name=signal.name,
                value=signal.raw_value,
                weight=(signal.score / signal.raw_value) if signal.raw_value else 0.0,
            )
            for signal in metric.risk_signals
        )

    @staticmethod
    def _summary_for(metric: FileArchitectureMetrics) -> str:
        clauses = [f"{metric.path} carries a risk score of {metric.risk_score:.2f}"]
        if metric.imported_by_count:
            clauses.append(f"it is imported by {metric.imported_by_count} tracked files")
        if metric.public_symbol_count:
            clauses.append(f"it exposes {metric.public_symbol_count} public symbols")
        if metric.line_count:
            clauses.append(f"it spans {metric.line_count} lines")
        return ", ".join(clauses) + "."


def build_default_describe_file_import_hotspots_query() -> DescribeFileImportHotspotsQuery:
    return DescribeFileImportHotspotsQuery(
        build_dependency_map_query=build_default_build_dependency_map_query(),
    )


def build_default_explain_hotspot_query() -> ExplainHotspotQuery:
    return ExplainHotspotQuery(
        build_dependency_map_query=build_default_build_dependency_map_query(),
    )


describe_file_import_hotspots = build_default_describe_file_import_hotspots_query().describe
explain_hotspot = build_default_explain_hotspot_query().explain

__all__ = [
    "DescribeFileImportHotspotsQuery",
    "ExplainHotspotQuery",
    "describe_file_import_hotspots",
    "explain_hotspot",
]
