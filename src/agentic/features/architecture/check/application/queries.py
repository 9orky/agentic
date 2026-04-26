from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from ...map.application import BuildDependencyMapQuery, DependencyMapBuildError, build_default_build_dependency_map_query
from ...map.domain import ArchitectureConfigError, EdgeRuleViolation, FlowViolation
from ...map.infrastructure import ExtractorRuntime
from ..domain import (
    ArchitecturePolicyEvaluator,
    ArchitectureReport,
    CheckerError,
    ViolationGroup,
)
from ..infrastructure import DotRenderer, dot_renderer


@dataclass(frozen=True)
class BuildArchitectureReportResult:
    report: ArchitectureReport
    dot_report: str
    violation_groups: tuple[ViolationGroup, ...]

    @property
    def check_error(self) -> str | None:
        return self.report.check_error

    @property
    def violations(self) -> tuple[EdgeRuleViolation | FlowViolation, ...]:
        return self.report.violations

    @property
    def files_found(self) -> int:
        return self.report.files_found

    @property
    def files_excluded(self) -> int:
        return self.report.files_excluded

    @property
    def files_checked(self) -> int:
        return self.report.files_checked

    def to_json_dict(self) -> dict[str, object]:
        return self.report.to_json_dict()


class BuildArchitectureReportQuery:
    def __init__(
        self,
        *,
        build_dependency_map_query: BuildDependencyMapQuery,
        architecture_policy_evaluator: ArchitecturePolicyEvaluator,
        dot_renderer: DotRenderer,
    ) -> None:
        self._build_dependency_map_query = build_dependency_map_query
        self._architecture_policy_evaluator = architecture_policy_evaluator
        self._dot_renderer = dot_renderer

    def execute(
        self,
        project_root: Path,
        explicit_config_path: str | None = None,
        *,
        extractor_runtime: ExtractorRuntime | None = None,
    ) -> BuildArchitectureReportResult:
        report = self._build_report(
            project_root,
            explicit_config_path,
            extractor_runtime=extractor_runtime,
        )
        return BuildArchitectureReportResult(
            report=report,
            dot_report=self._dot_renderer.render_report(report),
            violation_groups=self._build_violation_groups(report),
        )

    def _build_report(
        self,
        project_root: Path,
        explicit_config_path: str | None = None,
        *,
        extractor_runtime: ExtractorRuntime | None = None,
    ) -> ArchitectureReport:
        try:
            dependency_map_result = self._build_dependency_map_query.execute(
                project_root,
                explicit_config_path,
                extractor_runtime=extractor_runtime,
            )
        except ArchitectureConfigError as exc:
            raise CheckerError(str(exc)) from exc
        except DependencyMapBuildError as exc:
            return ArchitectureReport(
                project_root=project_root,
                config_path=exc.load_result.path,
                config_format=exc.load_result.source_format,
                language=exc.load_result.config.language,
                runtime_command=exc.runtime_command,
                check_error=str(exc),
            )

        graph = dependency_map_result.graph
        violations = tuple(
            self._architecture_policy_evaluator.evaluate(
                graph,
                dependency_map_result.load_result.config,
            )
        )

        return ArchitectureReport(
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

    def _build_violation_groups(
        self,
        report: ArchitectureReport,
    ) -> tuple[ViolationGroup, ...]:
        groups: dict[str, list[str]] = {}
        order: list[str] = []

        for violation in report.violations:
            title = self._group_name(violation)
            if title not in groups:
                groups[title] = []
                order.append(title)
            groups[title].append(self._render_compact_violation(violation))

        return tuple(
            ViolationGroup(title=title, entries=tuple(groups[title]))
            for title in order
        )

    def _group_name(self, violation: EdgeRuleViolation | FlowViolation) -> str:
        if isinstance(violation, EdgeRuleViolation):
            return "Edge Rule Violations"

        names = {
            "backward-flow": "Backward Flow Violations",
            "no-reentry": "No Re-Entry Violations",
            "no-cycles": "Cycle Violations",
        }
        return names.get(violation.violation_type, "Flow Violations")

    def _render_compact_violation(
        self,
        violation: EdgeRuleViolation | FlowViolation,
    ) -> str:
        if isinstance(violation, EdgeRuleViolation):
            return (
                f"{violation.source_id} -> [{violation.target_id}] "
                f"blocked by {violation.source_pattern} -> {violation.target_pattern}"
            )

        path_parts = list(violation.path)
        path_parts[violation.violation_index] = f"[{path_parts[violation.violation_index]}]"
        return f"{' -> '.join(path_parts)}  {violation.violation_type}"


@dataclass(frozen=True)
class ArchitectureSummary:
    project_root: Path
    config_path: Path
    config_format: str
    language: str
    runtime_command: str
    files_found: int = 0
    files_excluded: int = 0
    files_checked: int = 0
    violations: tuple[str, ...] = ()
    check_error: str | None = None


class DescribeArchitectureQuery:
    def __init__(
        self,
        *,
        build_architecture_report_query: BuildArchitectureReportQuery,
    ) -> None:
        self._build_architecture_report_query = build_architecture_report_query

    def describe(
        self,
        project_root: Path,
        explicit_config_path: str | None = None,
        *,
        extractor_runtime: ExtractorRuntime | None = None,
    ) -> ArchitectureSummary:
        result = self._build_architecture_report_query.execute(
            project_root,
            explicit_config_path,
            extractor_runtime=extractor_runtime,
        )
        return ArchitectureSummary(
            project_root=result.report.project_root,
            config_path=result.report.config_path,
            config_format=result.report.config_format,
            language=result.report.language,
            runtime_command=result.report.runtime_command,
            files_found=result.report.files_found,
            files_excluded=result.report.files_excluded,
            files_checked=result.report.files_checked,
            violations=tuple(self._render_violation(violation) for violation in result.report.violations),
            check_error=result.report.check_error,
        )

    def _render_violation(self, violation: EdgeRuleViolation | FlowViolation) -> str:
        if isinstance(violation, EdgeRuleViolation):
            return (
                f"[VIOLATION] {violation.source_id}\n"
                f"  -> Layer '{violation.source_pattern}' cannot depend on '{violation.target_pattern}'\n"
                f"  -> Offending import: '{violation.target_id}'"
            )

        path_text = " -> ".join(violation.path)
        highlighted_node = violation.path[violation.violation_index]
        return (
            f"[VIOLATION] {violation.violation_type}\n"
            f"  -> Path: {path_text}\n"
            f"  -> Violation point: '{highlighted_node}'\n"
            f"  -> Reason: {violation.message}"
        )


def build_default_build_architecture_report_query() -> BuildArchitectureReportQuery:
    return BuildArchitectureReportQuery(
        build_dependency_map_query=build_default_build_dependency_map_query(),
        architecture_policy_evaluator=ArchitecturePolicyEvaluator(),
        dot_renderer=dot_renderer,
    )


def build_default_describe_architecture_query() -> DescribeArchitectureQuery:
    return DescribeArchitectureQuery(
        build_architecture_report_query=build_default_build_architecture_report_query(),
    )


build_architecture_report = build_default_build_architecture_report_query().execute
describe_architecture = build_default_describe_architecture_query().describe

__all__ = [
    "ArchitectureSummary",
    "BuildArchitectureReportQuery",
    "BuildArchitectureReportResult",
    "DescribeArchitectureQuery",
    "build_architecture_report",
    "describe_architecture",
]
