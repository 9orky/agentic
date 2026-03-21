from dataclasses import dataclass

from .node_selector import NodeSelector


@dataclass(frozen=True)
class DependencyRule:
    name: str
    source: NodeSelector
    target: NodeSelector
    decision: str
    allow_same_match: bool = False
