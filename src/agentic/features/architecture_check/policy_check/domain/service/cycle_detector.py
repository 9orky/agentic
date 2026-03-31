from __future__ import annotations

from ....dependency_map.domain import DependencyGraph


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
                    cycle = tuple(stack[stack_index[next_id]:] + [next_id])
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
        rotations = [tuple(ring[index:] + ring[:index])
                     for index in range(len(ring))]
        smallest = min(rotations)
        return smallest + (smallest[0],)
