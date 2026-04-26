from __future__ import annotations

from dataclasses import dataclass, field

from .value_object import FileMetricSet


@dataclass(frozen=True)
class Node:
    id: str
    kind: str = "file"


@dataclass(frozen=True)
class Edge:
    from_id: str
    to_id: str
    kind: str = "import"


@dataclass
class DependencyGraph:
    nodes: dict[str, Node] = field(default_factory=dict)
    edges: list[Edge] = field(default_factory=list)
    _outgoing_by_node: dict[str, list[Edge]] = field(default_factory=dict)

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


@dataclass(frozen=True)
class FileSymbolInventory:
    path: str
    classes: tuple[str, ...] = ()
    functions: tuple[str, ...] = ()
    methods: tuple[str, ...] = ()
    metrics: FileMetricSet | None = None

    @property
    def symbol_count(self) -> int:
        return len(self.classes) + len(self.functions) + len(self.methods)


@dataclass(frozen=True)
class SymbolGraph:
    files: tuple[FileSymbolInventory, ...]

    def inventory_for(self, path: str) -> FileSymbolInventory | None:
        for file_inventory in self.files:
            if file_inventory.path == path:
                return file_inventory
        return None


__all__ = ["DependencyGraph", "Edge", "FileSymbolInventory", "Node", "SymbolGraph"]
