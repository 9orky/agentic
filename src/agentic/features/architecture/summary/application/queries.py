from __future__ import annotations

from pathlib import Path

from ...map.application import (
    BuildDependencyMapQuery,
    DependencyMapBuildError,
    build_default_build_dependency_map_query,
)
from ...map.application.metrics import derive_file_architecture_metrics
from ...map.domain import ArchitectureConfigError, CheckerError
from ...map.infrastructure import ExtractorRuntime
from ..domain import ArchitectureSummaryReport, ReadingPriority, RiskFinding, SummarySection


class DescribeArchitectureSummaryQuery:
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
        top: int = 10,
        extractor_runtime: ExtractorRuntime | None = None,
    ) -> ArchitectureSummaryReport:
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

        metrics = derive_file_architecture_metrics(dependency_map_result)
        highest_risk = sorted(metrics, key=lambda item: (-item.risk_score, item.path))[:top]
        incoming_hubs = sorted(
            metrics,
            key=lambda item: (-item.imported_by_count, -item.risk_score, item.path),
        )[:top]

        sections = (
            SummarySection(
                title="What This Summary Covers",
                entries=(
                    "A quick reading order for the files that shape architecture decisions first.",
                    "The highest-risk files where agent edits are most likely to become expensive.",
                    "The strongest dependency hubs in the tracked graph.",
                ),
            ),
            SummarySection(
                title="Highest-Risk Files",
                entries=tuple(
                    f"{item.path} ({item.risk_score:.2f}) - {', '.join(item.dominant_signals) or 'low graph pressure'}"
                    for item in highest_risk
                ),
            ),
            SummarySection(
                title="Dependency Hubs",
                entries=tuple(
                    f"{item.path} - imported by {item.imported_by_count} files, imports {item.imports_count}"
                    for item in incoming_hubs
                ),
            ),
        )

        reading_priorities = tuple(
            ReadingPriority(
                path=item.path,
                reason=(
                    f"Read early because it combines {item.imported_by_count} incoming imports "
                    f"with {item.public_symbol_count} public symbols."
                ),
                risk_level=_risk_level_for(item.risk_score),
            )
            for item in highest_risk[: min(top, 5)]
        )

        risk_findings = tuple(
            RiskFinding(
                path=item.path,
                summary=(
                    f"Risk {item.risk_score:.2f} driven by {', '.join(item.dominant_signals) or 'general graph pressure'}."
                ),
                risk_level=_risk_level_for(item.risk_score),
            )
            for item in highest_risk[: min(top, 5)]
        )

        return ArchitectureSummaryReport(
            sections=sections,
            reading_priorities=reading_priorities,
            risk_findings=risk_findings,
        )


def _risk_level_for(score: float) -> str:
    if score >= 20:
        return "high"
    if score >= 10:
        return "medium"
    return "low"


def build_default_describe_architecture_summary_query() -> DescribeArchitectureSummaryQuery:
    return DescribeArchitectureSummaryQuery(
        build_dependency_map_query=build_default_build_dependency_map_query(),
    )


describe_architecture_summary = build_default_describe_architecture_summary_query().describe

__all__ = ["DescribeArchitectureSummaryQuery", "describe_architecture_summary"]
