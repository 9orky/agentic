from __future__ import annotations

from ....domain import DependencyGraph, ExtractedFile, NodeSelector


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


__all__ = ["DependencyGraphBuilder"]
