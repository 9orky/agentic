from __future__ import annotations

from .edge import Edge
from .node import Node


class DependencyGraph:
    def __init__(self) -> None:
        self.nodes: dict[str, Node] = {}
        self.edges: list[Edge] = []
        self._outgoing_by_node: dict[str, list[Edge]] = {}

    def add_node(self, node_id: str, *, kind: str = "file") -> None:
        self.nodes.setdefault(node_id, Node(id=node_id, kind=kind))
        self._outgoing_by_node.setdefault(node_id, [])

    def add_edge(self, from_id: str, to_id: str, *, kind: str = "import") -> None:
        self.add_node(from_id)
        self.add_node(to_id)
        edge = Edge(from_id=from_id, to_id=to_id, kind=kind)
        self.edges.append(edge)
        self._outgoing_by_node[from_id].append(edge)

    def outgoing(self, node_id: str) -> tuple[Edge, ...]:
        return tuple(self._outgoing_by_node.get(node_id, ()))

    def node_ids(self) -> tuple[str, ...]:
        return tuple(self.nodes.keys())
