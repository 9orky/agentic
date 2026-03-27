from __future__ import annotations

from ...application.queries import ViolationGroup


class GroupedViolationView:
    def render(self, groups: tuple[ViolationGroup, ...]) -> str:
        lines: list[str] = []
        for group in groups:
            lines.append(f"{group.title}:")
            for entry in group.entries:
                lines.append(f"- {entry}")

        return "\n".join(lines)
