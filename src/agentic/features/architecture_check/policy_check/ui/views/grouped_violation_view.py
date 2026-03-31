from __future__ import annotations

from typing import Protocol


class ViolationGroupLike(Protocol):
    title: str
    entries: tuple[str, ...]


class GroupedViolationView:
    def render(self, groups: tuple[ViolationGroupLike, ...]) -> str:
        lines: list[str] = []
        for group in groups:
            lines.append(f"{group.title}:")
            for entry in group.entries:
                lines.append(f"- {entry}")

        return "\n".join(lines)
