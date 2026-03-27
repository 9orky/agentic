from __future__ import annotations

from ..entity import DependencyGraph
from ..value_object import FlowAnalyzerConfig, FlowViolation


class BackwardFlowAnalyzer:
    def analyze(self, graph: DependencyGraph, tags: dict[str, set[str]], config: FlowAnalyzerConfig) -> list[FlowViolation]:
        violations: list[FlowViolation] = []
        seen: set[tuple[str, int | None]] = set()

        for start_node in self._root_nodes(graph):
            self._walk(
                graph,
                tags,
                config,
                start_node,
                [self._layer_index(
                    tags.get(start_node, set()), config.layers)],
                [start_node],
                seen,
                violations,
            )

        return self._dedupe(violations)

    def _walk(
        self,
        graph: DependencyGraph,
        tags: dict[str, set[str]],
        config: FlowAnalyzerConfig,
        node_id: str,
        layer_stack: list[int | None],
        path: list[str],
        seen: set[tuple[str, int | None]],
        violations: list[FlowViolation],
    ) -> None:
        current_layer = layer_stack[-1]
        state_key = (node_id, current_layer)
        if state_key in seen:
            return

        seen.add(state_key)

        for edge in graph.outgoing(node_id):
            next_id = edge.to_id
            next_layer = self._layer_index(
                tags.get(next_id, set()), config.layers)

            if current_layer is not None and next_layer is not None and next_layer < current_layer:
                violations.append(
                    FlowViolation(
                        violation_type="backward-flow",
                        path=tuple(path + [next_id]),
                        violation_index=len(path),
                        rule_name="analyzer:backward-flow",
                        message="layer order violated",
                    )
                )
                continue

            resolved_next_layer = next_layer if next_layer is not None else current_layer
            self._walk(
                graph,
                tags,
                config,
                next_id,
                layer_stack + [resolved_next_layer],
                path + [next_id],
                seen,
                violations,
            )

    def _layer_index(self, node_tags: set[str], layers: tuple[str, ...]) -> int | None:
        for index, layer in enumerate(layers):
            if layer in node_tags:
                return index
        return None

    def _dedupe(self, violations: list[FlowViolation]) -> list[FlowViolation]:
        unique: list[FlowViolation] = []
        seen: set[tuple[str, tuple[str, ...], int]] = set()

        for violation in violations:
            key = (violation.violation_type, violation.path,
                   violation.violation_index)
            if key in seen:
                continue
            seen.add(key)
            unique.append(violation)

        return unique

    def _root_nodes(self, graph: DependencyGraph) -> tuple[str, ...]:
        incoming_counts = {node_id: 0 for node_id in graph.node_ids()}
        for edge in graph.edges:
            if edge.to_id in incoming_counts:
                incoming_counts[edge.to_id] += 1

        roots = tuple(sorted(node_id for node_id,
                      count in incoming_counts.items() if count == 0))
        if roots:
            return roots
        return tuple(sorted(graph.node_ids()))
