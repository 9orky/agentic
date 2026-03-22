from __future__ import annotations

from ...domain.entity import DependencyGraph
from ...domain.service import ArchitecturePolicyEvaluator
from ...domain.value_object import ArchitectureCheckConfig, EdgeRuleViolation, FlowViolation


class ArchitectureEvaluator:
    def __init__(self, policy_evaluator: ArchitecturePolicyEvaluator | None = None) -> None:
        self._policy_evaluator = policy_evaluator or ArchitecturePolicyEvaluator()

    def evaluate(
        self,
        graph: DependencyGraph,
        config: ArchitectureCheckConfig,
    ) -> list[EdgeRuleViolation | FlowViolation]:
        return self._policy_evaluator.evaluate(graph, config)


evaluate_architecture = ArchitectureEvaluator().evaluate

__all__ = ["ArchitectureEvaluator", "evaluate_architecture"]
