from __future__ import annotations

from ...domain.entity import DependencyGraph
from ...domain.value_object import ExtractedFile, NodeSelector


class DependencyGraphBuilder:
    def build(self, architecture_map: dict[str, ExtractedFile]) -> DependencyGraph:
        graph = DependencyGraph()

        for file_path, extracted_file in architecture_map.items():
            graph.add_node(file_path)
            for imported_reference in extracted_file.imports:
                normalized_import = NodeSelector.normalize_import_reference(
                    imported_reference)
                if not normalized_import:
                    continue
                graph.add_edge(file_path, normalized_import)

        return graph


build_dependency_graph = DependencyGraphBuilder().build

__all__ = ["DependencyGraphBuilder", "build_dependency_graph"]
