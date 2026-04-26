from __future__ import annotations

from ...map.domain import (
    ArchitectureConfig,
    DependencyGraph,
    DependencyRule,
    EdgeRuleViolation,
    FlowAnalyzerConfig,
    FlowViolation,
    NodeSelector,
    TagRule,
)


class CycleDetector:
    def detect(self, graph: DependencyGraph, scoped_node_ids: set[str]) -> list[tuple[str, ...]]:
        visited: set[str] = set()
        stack: list[str] = []
        stack_index: dict[str, int] = {}
        cycles: list[tuple[str, ...]] = []
        emitted: set[tuple[str, ...]] = set()

        def dfs(node_id: str) -> None:
            visited.add(node_id)
            stack_index[node_id] = len(stack)
            stack.append(node_id)

            for edge in graph.outgoing(node_id):
                next_id = edge.to_id
                if next_id not in scoped_node_ids:
                    continue

                if next_id in stack_index:
                    cycle = tuple(stack[stack_index[next_id] :] + [next_id])
                    canonical = self._canonicalize(cycle)
                    if canonical not in emitted:
                        emitted.add(canonical)
                        cycles.append(cycle)
                    continue

                if next_id not in visited:
                    dfs(next_id)

            stack.pop()
            stack_index.pop(node_id, None)

        for node_id in sorted(scoped_node_ids):
            if node_id not in visited:
                dfs(node_id)

        return cycles

    def _canonicalize(self, cycle: tuple[str, ...]) -> tuple[str, ...]:
        if len(cycle) <= 1:
            return cycle

        ring = list(cycle[:-1])
        rotations = [tuple(ring[index:] + ring[:index]) for index in range(len(ring))]
        smallest = min(rotations)
        return smallest + (smallest[0],)


class BackwardFlowAnalyzer:
    def analyze(
        self,
        graph: DependencyGraph,
        tags: dict[str, set[str]],
        config: FlowAnalyzerConfig,
    ) -> list[FlowViolation]:
        violations: list[FlowViolation] = []
        seen: set[tuple[str, int | None]] = set()

        for start_node in self._root_nodes(graph):
            self._walk(
                graph,
                tags,
                config,
                start_node,
                [self._layer_index(tags.get(start_node, set()), config.layers)],
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
            next_layer = self._layer_index(tags.get(next_id, set()), config.layers)

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
            key = (violation.violation_type, violation.path, violation.violation_index)
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

        roots = tuple(sorted(node_id for node_id, count in incoming_counts.items() if count == 0))
        if roots:
            return roots
        return tuple(sorted(graph.node_ids()))


class NoReentryAnalyzer:
    def analyze(
        self,
        graph: DependencyGraph,
        tags: dict[str, set[str]],
        config: FlowAnalyzerConfig,
    ) -> list[FlowViolation]:
        violations: list[FlowViolation] = []
        seen: set[tuple[str, str]] = set()

        for start_node in self._root_nodes(graph):
            self._walk(
                graph,
                tags,
                config,
                start_node,
                self._module_state_for_start(start_node, tags, config.module_tag),
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

    def _module_state_for_start(
        self,
        node_id: str,
        tags: dict[str, set[str]],
        module_tag: str,
    ) -> str:
        if module_tag in tags.get(node_id, set()):
            return "INSIDE_MODULE"
        return "OUTSIDE"

    def _dedupe(self, violations: list[FlowViolation]) -> list[FlowViolation]:
        unique: list[FlowViolation] = []
        seen: set[tuple[str, tuple[str, ...], int]] = set()

        for violation in violations:
            key = (violation.violation_type, violation.path, violation.violation_index)
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

        roots = tuple(sorted(node_id for node_id, count in incoming_counts.items() if count == 0))
        if roots:
            return roots
        return tuple(sorted(graph.node_ids()))


class NoCyclesAnalyzer:
    def __init__(self, cycle_detector: CycleDetector | None = None) -> None:
        self._cycle_detector = cycle_detector or CycleDetector()

    def analyze(
        self,
        graph: DependencyGraph,
        tags: dict[str, set[str]],
        config: FlowAnalyzerConfig,
    ) -> list[FlowViolation]:
        scoped_node_ids = {
            node_id for node_id, node_tags in tags.items() if config.module_tag in node_tags
        }
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


class ArchitecturePolicyEvaluator:
    ANALYZERS = {
        "backward-flow": BackwardFlowAnalyzer,
        "no-reentry": NoReentryAnalyzer,
        "no-cycles": NoCyclesAnalyzer,
    }

    def evaluate(
        self,
        graph: DependencyGraph,
        config: ArchitectureConfig,
    ) -> list[EdgeRuleViolation | FlowViolation]:
        tag_rules = tuple(TagRule(name=rule.name, match=rule.match) for rule in config.rules.tags)
        tags = self._derive_tags(graph.node_ids(), tag_rules)

        violations: list[EdgeRuleViolation | FlowViolation] = []
        violations.extend(self._evaluate_edge_rules(graph, self._translate_boundary_rules(config), tags))

        flow_config = FlowAnalyzerConfig(
            layers=tuple(config.rules.flow.layers),
            module_tag=config.rules.flow.module_tag,
        )
        for analyzer in self._resolve_flow_analyzers(config):
            violations.extend(analyzer.analyze(graph, tags, flow_config))

        return violations

    def _resolve_flow_analyzers(
        self,
        config: ArchitectureConfig,
    ) -> tuple[BackwardFlowAnalyzer | NoReentryAnalyzer | NoCyclesAnalyzer, ...]:
        analyzers: list[BackwardFlowAnalyzer | NoReentryAnalyzer | NoCyclesAnalyzer] = []
        for analyzer_name in config.rules.flow.analyzers:
            analyzer_type = self.ANALYZERS.get(analyzer_name)
            if analyzer_type is None:
                continue
            analyzers.append(analyzer_type())
        return tuple(analyzers)

    def _translate_boundary_rules(
        self,
        config: ArchitectureConfig,
    ) -> tuple[DependencyRule, ...]:
        translated_rules: list[DependencyRule] = []

        for boundary in config.rules.boundaries:
            source_selector = NodeSelector(path_pattern=boundary.source, path_mode="scope")

            for disallowed_pattern in boundary.disallow:
                translated_rules.append(
                    DependencyRule(
                        name=f"boundary:{boundary.source}->{disallowed_pattern}:deny",
                        source=source_selector,
                        target=NodeSelector(path_pattern=disallowed_pattern, path_mode="scope"),
                        decision="deny",
                        allow_same_match=boundary.allow_same_match,
                    )
                )

            for allowed_pattern in boundary.allow:
                translated_rules.append(
                    DependencyRule(
                        name=f"boundary:{boundary.source}->{allowed_pattern}:allow",
                        source=source_selector,
                        target=NodeSelector(path_pattern=allowed_pattern, path_mode="exact"),
                        decision="allow",
                    )
                )

        return tuple(translated_rules)

    def _derive_tags(
        self,
        node_ids: tuple[str, ...],
        rules: tuple[TagRule, ...],
    ) -> dict[str, set[str]]:
        tags: dict[str, set[str]] = {}

        for node_id in node_ids:
            node_tags: set[str] = set()
            for rule in rules:
                selector = NodeSelector(path_pattern=rule.match, path_mode="scope")
                if selector.matches(node_id) is not None:
                    node_tags.add(rule.name)
            tags[node_id] = node_tags

        return tags

    def _evaluate_edge_rules(
        self,
        graph: DependencyGraph,
        rules: tuple[DependencyRule, ...],
        tags: dict[str, set[str]],
    ) -> list[EdgeRuleViolation]:
        violations: list[EdgeRuleViolation] = []

        for edge in graph.edges:
            matched_rule: DependencyRule | None = None

            for rule in rules:
                source_match = rule.source.matches(edge.from_id, tags)
                if source_match is None:
                    continue

                target_match = rule.target.matches(edge.to_id, tags)
                if target_match is None:
                    continue

                if (
                    rule.allow_same_match
                    and source_match.captures
                    and source_match.captures == target_match.captures
                ):
                    continue

                matched_rule = rule

            if matched_rule is None or matched_rule.decision != "deny":
                continue

            violations.append(
                EdgeRuleViolation(
                    source_id=edge.from_id,
                    target_id=edge.to_id,
                    source_pattern=matched_rule.source.path_pattern or "*",
                    target_pattern=matched_rule.target.path_pattern or "*",
                    rule_name=matched_rule.name,
                )
            )

        return violations


__all__ = [
    "ArchitecturePolicyEvaluator",
    "BackwardFlowAnalyzer",
    "CycleDetector",
    "NoCyclesAnalyzer",
    "NoReentryAnalyzer",
]
