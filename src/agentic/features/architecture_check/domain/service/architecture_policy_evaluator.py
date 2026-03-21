from __future__ import annotations

from .backward_flow_analyzer import BackwardFlowAnalyzer
from .no_cycles_analyzer import NoCyclesAnalyzer
from .no_reentry_analyzer import NoReentryAnalyzer
from ..entity import DependencyGraph
from ..value_object import ArchitectureCheckConfig, DependencyRule, EdgeRuleViolation, FlowAnalyzerConfig, FlowViolation, NodeSelector, TagRule


class ArchitecturePolicyEvaluator:
    ANALYZERS = {
        "backward-flow": BackwardFlowAnalyzer,
        "no-reentry": NoReentryAnalyzer,
        "no-cycles": NoCyclesAnalyzer,
    }

    def evaluate(self, graph: DependencyGraph, config: ArchitectureCheckConfig) -> list[EdgeRuleViolation | FlowViolation]:
        tag_rules = tuple(TagRule(name=rule.name, match=rule.match)
                          for rule in config.rules.tags)
        tags = self._derive_tags(graph.node_ids(), tag_rules)

        violations: list[EdgeRuleViolation | FlowViolation] = []
        violations.extend(self._evaluate_edge_rules(
            graph, self._translate_boundary_rules(config), tags))

        flow_config = FlowAnalyzerConfig(
            layers=tuple(config.rules.flow.layers),
            module_tag=config.rules.flow.module_tag,
        )
        for analyzer in self._resolve_flow_analyzers(config):
            violations.extend(analyzer.analyze(graph, tags, flow_config))

        return violations

    def _resolve_flow_analyzers(self, config: ArchitectureCheckConfig) -> tuple[BackwardFlowAnalyzer | NoReentryAnalyzer | NoCyclesAnalyzer, ...]:
        analyzers: list[BackwardFlowAnalyzer |
                        NoReentryAnalyzer | NoCyclesAnalyzer] = []
        for analyzer_name in config.rules.flow.analyzers:
            analyzer_type = self.ANALYZERS.get(analyzer_name)
            if analyzer_type is None:
                continue
            analyzers.append(analyzer_type())
        return tuple(analyzers)

    def _translate_boundary_rules(self, config: ArchitectureCheckConfig) -> tuple[DependencyRule, ...]:
        translated_rules: list[DependencyRule] = []

        for boundary in config.rules.boundaries:
            source_selector = NodeSelector(
                path_pattern=boundary.source, path_mode="scope")

            for disallowed_pattern in boundary.disallow:
                translated_rules.append(
                    DependencyRule(
                        name=f"boundary:{boundary.source}->{disallowed_pattern}:deny",
                        source=source_selector,
                        target=NodeSelector(
                            path_pattern=disallowed_pattern, path_mode="scope"),
                        decision="deny",
                        allow_same_match=boundary.allow_same_match,
                    )
                )

            for allowed_pattern in boundary.allow:
                translated_rules.append(
                    DependencyRule(
                        name=f"boundary:{boundary.source}->{allowed_pattern}:allow",
                        source=source_selector,
                        target=NodeSelector(
                            path_pattern=allowed_pattern, path_mode="exact"),
                        decision="allow",
                    )
                )

        return tuple(translated_rules)

    def _derive_tags(self, node_ids: tuple[str, ...], rules: tuple[TagRule, ...]) -> dict[str, set[str]]:
        tags: dict[str, set[str]] = {}

        for node_id in node_ids:
            node_tags: set[str] = set()
            for rule in rules:
                if NodeSelector(path_pattern=rule.match, path_mode="scope").matches(node_id) is not None:
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
