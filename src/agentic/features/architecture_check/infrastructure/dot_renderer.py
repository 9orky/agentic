from __future__ import annotations

from collections import OrderedDict

from ..domain.value_object import EdgeRuleViolation, FlowViolation


class ViolationDotRenderer:
    def render(self, violations: tuple[EdgeRuleViolation | FlowViolation, ...]) -> str:
        edges: OrderedDict[tuple[str, str], None] = OrderedDict()

        for violation in violations:
            for source_id, target_id in self._violation_edges(violation):
                edges[(source_id, target_id)] = None

        lines = ["digraph architecture_violations {", "  rankdir=LR;"]
        for source_id, target_id in edges:
            lines.append(f'  "{source_id}" -> "{target_id}";')
        lines.append("}")
        return "\n".join(lines)

    def _violation_edges(self, violation: EdgeRuleViolation | FlowViolation) -> tuple[tuple[str, str], ...]:
        if isinstance(violation, EdgeRuleViolation):
            return ((violation.source_id, violation.target_id),)

        return tuple(
            (violation.path[index], violation.path[index + 1])
            for index in range(len(violation.path) - 1)
        )
