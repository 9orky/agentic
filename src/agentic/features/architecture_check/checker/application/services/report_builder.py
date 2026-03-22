from __future__ import annotations

from pathlib import Path

from ...domain.value_object import ArchitectureCheckConfigError, CheckerError, EdgeRuleViolation, FlowViolation
from ...infrastructure import ExtractorRuntime, ExtractorSpecRegistry, ViolationDotRenderer
from ..queries.load_config import LoadConfigQuery
from .architecture_check_report import ArchitectureCheckReport
from .architecture_evaluator import ArchitectureEvaluator
from .dependency_graph_builder import DependencyGraphBuilder
from .runtime_registry import ExtractorRuntimeFactory
from .violation_group import ViolationGroup


class ArchitectureReportBuilder:
    def __init__(
        self,
        load_config_query: LoadConfigQuery | None = None,
        extractor_runtime_factory: ExtractorRuntimeFactory | None = None,
        extractor_spec_registry: ExtractorSpecRegistry | None = None,
        dependency_graph_builder: DependencyGraphBuilder | None = None,
        architecture_evaluator: ArchitectureEvaluator | None = None,
        violation_dot_renderer: ViolationDotRenderer | None = None,
    ) -> None:
        self._load_config_query = load_config_query or LoadConfigQuery()
        self._extractor_runtime_factory = extractor_runtime_factory or ExtractorRuntimeFactory()
        self._extractor_spec_registry = extractor_spec_registry or ExtractorSpecRegistry()
        self._dependency_graph_builder = dependency_graph_builder or DependencyGraphBuilder()
        self._architecture_evaluator = architecture_evaluator or ArchitectureEvaluator()
        self._violation_dot_renderer = violation_dot_renderer or ViolationDotRenderer()

    def build(
        self,
        project_root: Path,
        explicit_config_path: str | None = None,
        *,
        extractor_runtime: ExtractorRuntime | None = None,
    ) -> ArchitectureCheckReport:
        runtime = extractor_runtime or self._extractor_runtime_factory.create()

        try:
            load_result = self._load_config_query.load(
                project_root, explicit_config_path)
        except ArchitectureCheckConfigError as exc:
            raise CheckerError(str(exc)) from exc

        try:
            extractor_spec = self._extractor_spec_registry.get(
                load_result.config.language)
        except CheckerError as exc:
            raise CheckerError(str(exc)) from exc

        try:
            extraction_result = runtime.run(
                extractor_spec,
                project_root,
                load_result.config.exclusions,
            )
        except CheckerError as exc:
            return ArchitectureCheckReport(
                project_root=project_root,
                config_path=load_result.path,
                config_format=load_result.source_format,
                language=load_result.config.language,
                runtime_command=extractor_spec.command,
                check_error=str(exc),
            )

        graph = self._dependency_graph_builder.build(extraction_result.files)
        violations = tuple(self._architecture_evaluator.evaluate(
            graph, load_result.config))

        return ArchitectureCheckReport(
            project_root=project_root,
            config_path=load_result.path,
            config_format=load_result.source_format,
            language=load_result.config.language,
            runtime_command=extractor_spec.command,
            files_found=extraction_result.summary.files_found,
            files_excluded=extraction_result.summary.files_excluded,
            files_checked=extraction_result.summary.files_checked,
            violations=violations,
        )

    def build_violation_groups(self, report: ArchitectureCheckReport) -> tuple[ViolationGroup, ...]:
        groups: dict[str, list[str]] = {}
        order: list[str] = []

        for violation in report.violations:
            title = self._group_name(violation)
            if title not in groups:
                groups[title] = []
                order.append(title)
            groups[title].append(self._render_compact_violation(violation))

        return tuple(ViolationGroup(title=title, entries=tuple(groups[title])) for title in order)

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


_ARCHITECTURE_REPORT_BUILDER = ArchitectureReportBuilder()
build_architecture_report = _ARCHITECTURE_REPORT_BUILDER.build
build_violation_groups = _ARCHITECTURE_REPORT_BUILDER.build_violation_groups
build_dot_report = _ARCHITECTURE_REPORT_BUILDER.build_dot_report

__all__ = [
    "ArchitectureReportBuilder",
    "build_architecture_report",
    "build_dot_report",
    "build_violation_groups",
]
