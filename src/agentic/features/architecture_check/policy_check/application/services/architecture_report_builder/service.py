from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .....dependency_map.application import BuildDependencyMapQuery, DependencyMapBuildError, build_default_build_dependency_map_query
from ....domain import ArchitecturePolicyEvaluator, ArchitectureCheckConfigError, CheckerError, EdgeRuleViolation, FlowViolation
from ....infrastructure import ViolationDotRenderer
from .architecture_check_report import ArchitectureCheckReport
from .architecture_evaluator import ArchitectureEvaluator


@dataclass(frozen=True)
class ArchitectureReportArtifacts:
    report: ArchitectureCheckReport
    dot_report: str
    violation_groups: tuple[tuple[str, tuple[str, ...]], ...]


class ArchitectureReportBuilder:
    def __init__(
        self,
        *,
        build_dependency_map_query: BuildDependencyMapQuery,
        architecture_evaluator: ArchitectureEvaluator,
        violation_dot_renderer: ViolationDotRenderer,
    ) -> None:
        self._build_dependency_map_query = build_dependency_map_query
        self._architecture_evaluator = architecture_evaluator
        self._violation_dot_renderer = violation_dot_renderer

    def build(
        self,
        project_root: Path,
        explicit_config_path: str | None = None,
        *,
        extractor_runtime: object | None = None,
    ) -> ArchitectureCheckReport:
        try:
            dependency_map_result = self._build_dependency_map_query.execute(
                project_root,
                explicit_config_path,
                extractor_runtime=extractor_runtime,
            )
        except ArchitectureCheckConfigError as exc:
            raise CheckerError(str(exc)) from exc

        except DependencyMapBuildError as exc:
            return ArchitectureCheckReport(
                project_root=project_root,
                config_path=exc.load_result.path,
                config_format=exc.load_result.source_format,
                language=exc.load_result.config.language,
                runtime_command=exc.runtime_command,
                check_error=str(exc),
            )

        graph = dependency_map_result.graph
        violations = tuple(self._architecture_evaluator.evaluate(
            graph, dependency_map_result.load_result.config))

        return ArchitectureCheckReport(
            project_root=project_root,
            config_path=dependency_map_result.load_result.path,
            config_format=dependency_map_result.load_result.source_format,
            language=dependency_map_result.load_result.config.language,
            runtime_command=dependency_map_result.runtime_command,
            files_found=dependency_map_result.extraction_result.summary.files_found,
            files_excluded=dependency_map_result.extraction_result.summary.files_excluded,
            files_checked=dependency_map_result.extraction_result.summary.files_checked,
            violations=violations,
        )

    def build_artifacts(
        self,
        project_root: Path,
        explicit_config_path: str | None = None,
        *,
        extractor_runtime: object | None = None,
    ) -> ArchitectureReportArtifacts:
        report = self.build(
            project_root,
            explicit_config_path,
            extractor_runtime=extractor_runtime,
        )
        return ArchitectureReportArtifacts(
            report=report,
            dot_report=self.build_dot_report(report),
            violation_groups=self._build_violation_group_data(report),
        )

    def _build_violation_group_data(self, report: ArchitectureCheckReport) -> tuple[tuple[str, tuple[str, ...]], ...]:
        groups: dict[str, list[str]] = {}
        order: list[str] = []

        for violation in report.violations:
            title = self._group_name(violation)
            if title not in groups:
                groups[title] = []
                order.append(title)
            groups[title].append(self._render_compact_violation(violation))

        return tuple((title, tuple(groups[title])) for title in order)

    def build_dot_report(self, report: ArchitectureCheckReport) -> str:
        return self._violation_dot_renderer.render(report.violations)

    def _group_name(self, violation: EdgeRuleViolation | FlowViolation) -> str:
        if isinstance(violation, EdgeRuleViolation):
            return "Edge Rule Violations"

        names = {
            "backward-flow": "Backward Flow Violations",
            "no-reentry": "No Re-Entry Violations",
            "no-cycles": "Cycle Violations",
        }
        return names.get(violation.violation_type, "Flow Violations")

    def _render_compact_violation(self, violation: EdgeRuleViolation | FlowViolation) -> str:
        if isinstance(violation, EdgeRuleViolation):
            return (
                f"{violation.source_id} -> [{violation.target_id}] "
                f"blocked by {violation.source_pattern} -> {violation.target_pattern}"
            )

        path_parts = list(violation.path)
        path_parts[violation.violation_index] = f"[{path_parts[violation.violation_index]}]"
        return f"{' -> '.join(path_parts)}  {violation.violation_type}"


def build_default_architecture_report_builder() -> ArchitectureReportBuilder:
    return ArchitectureReportBuilder(
        build_dependency_map_query=build_default_build_dependency_map_query(),
        architecture_evaluator=ArchitectureEvaluator(
            policy_evaluator=ArchitecturePolicyEvaluator(),
        ),
        violation_dot_renderer=ViolationDotRenderer(),
    )


__all__ = ["ArchitectureReportBuilder",
           "build_default_architecture_report_builder"]
