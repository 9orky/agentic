from __future__ import annotations

from .cycle_detector import CycleDetector
from ....dependency_map.domain import DependencyGraph, FlowAnalyzerConfig, FlowViolation


class NoCyclesAnalyzer:
    def __init__(self, cycle_detector: CycleDetector | None = None) -> None:
        self._cycle_detector = cycle_detector or CycleDetector()

    def analyze(self, graph: DependencyGraph, tags: dict[str, set[str]], config: FlowAnalyzerConfig) -> list[FlowViolation]:
        scoped_node_ids = {node_id for node_id, node_tags in tags.items(
        ) if config.module_tag in node_tags}
        cycles = self._cycle_detector.detect(graph, scoped_node_ids)
        return [
            FlowViolation(
                violation_type="no-cycles",
                path=cycle,
                violation_index=len(cycle) - 1,
                rule_name="analyzer:no-cycles",
                message="module cycle detected",
            )
            for cycle in cycles
        ]
