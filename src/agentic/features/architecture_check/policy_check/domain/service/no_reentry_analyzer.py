from __future__ import annotations

from ....dependency_map.domain import DependencyGraph, FlowAnalyzerConfig, FlowViolation


class NoReentryAnalyzer:
    def analyze(self, graph: DependencyGraph, tags: dict[str, set[str]], config: FlowAnalyzerConfig) -> list[FlowViolation]:
        violations: list[FlowViolation] = []
        seen: set[tuple[str, str]] = set()

        for start_node in self._root_nodes(graph):
            self._walk(
                graph,
                tags,
                config,
                start_node,
                self._module_state_for_start(
                    start_node, tags, config.module_tag),
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
        state: str,
        path: list[str],
        seen: set[tuple[str, str]],
        violations: list[FlowViolation],
    ) -> None:
        state_key = (node_id, state)
        if state_key in seen:
            return

        seen.add(state_key)

        for edge in graph.outgoing(node_id):
            next_id = edge.to_id
            next_is_module = config.module_tag in tags.get(next_id, set())
            next_state = state

            if state == "OUTSIDE":
                if next_is_module:
                    next_state = "INSIDE_MODULE"
            elif state == "INSIDE_MODULE":
                if not next_is_module:
                    next_state = "LEFT_MODULE"
            elif state == "LEFT_MODULE" and next_is_module:
                violations.append(
                    FlowViolation(
                        violation_type="no-reentry",
                        path=tuple(path + [next_id]),
                        violation_index=len(path),
                        rule_name="analyzer:no-reentry",
                        message="module layer re-entered after exit",
                    )
                )
                continue

            self._walk(
                graph,
                tags,
                config,
                next_id,
                next_state,
                path + [next_id],
                seen,
                violations,
            )

    def _module_state_for_start(self, node_id: str, tags: dict[str, set[str]], module_tag: str) -> str:
        if module_tag in tags.get(node_id, set()):
            return "INSIDE_MODULE"
        return "OUTSIDE"

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
