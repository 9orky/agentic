from __future__ import annotations

from ...domain.value_object import EdgeRuleViolation, FlowViolation


class ViolationRenderer:
    def render(self, violation: EdgeRuleViolation | FlowViolation) -> str:
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

    def format(self, violation: EdgeRuleViolation | FlowViolation) -> str:
        return self.render(violation)


_VIOLATION_RENDERER = ViolationRenderer()
render_violation = _VIOLATION_RENDERER.render
format_violation = _VIOLATION_RENDERER.format

__all__ = ["ViolationRenderer", "format_violation", "render_violation"]
