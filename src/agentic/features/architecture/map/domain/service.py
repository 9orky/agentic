from __future__ import annotations

from .entity import DependencyGraph
from .value_object import ExtractedFile, NodeSelector


class DependencyGraphBuilder:
    def build(self, extracted_files: dict[str, ExtractedFile]) -> DependencyGraph:
        graph = DependencyGraph()

        for file_path, extracted_file in extracted_files.items():
            graph.add_node(file_path)
            for imported_reference in extracted_file.imports:
                normalized_import = NodeSelector.normalize_import_reference(imported_reference)
                if not normalized_import:
                    continue
                graph.add_edge(file_path, normalized_import)

        return graph


__all__ = ["DependencyGraphBuilder"]
