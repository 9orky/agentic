from __future__ import annotations

from .....dependency_map.domain import ArchitectureCheckConfig, DependencyGraph, EdgeRuleViolation, FlowViolation
from ....domain import ArchitecturePolicyEvaluator


class ArchitectureEvaluator:
    def __init__(self, *, policy_evaluator: ArchitecturePolicyEvaluator) -> None:
        self._policy_evaluator = policy_evaluator

    def evaluate(
        self,
        graph: DependencyGraph,
        config: ArchitectureCheckConfig,
    ) -> list[EdgeRuleViolation | FlowViolation]:
        return self._policy_evaluator.evaluate(graph, config)


__all__ = ["ArchitectureEvaluator"]
