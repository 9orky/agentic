from __future__ import annotations

from typing import Protocol


class ViolationGroupLike(Protocol):
    @property
    def title(self) -> str: ...

    @property
    def entries(self) -> tuple[str, ...]: ...


class CheckSummaryPresenter:
    def render(self, files_found: int, files_excluded: int, files_checked: int) -> str:
        return "\n".join(
            [
                "Check Summary:",
                f"- Files found in scope: {files_found}",
                f"- Files excluded by rules: {files_excluded}",
                f"- Files checked: {files_checked}",
            ]
        )


class GroupedViolationView:
    def render(self, groups: tuple[ViolationGroupLike, ...]) -> str:
        lines: list[str] = []
        for group in groups:
            lines.append(f"{group.title}:")
            for entry in group.entries:
                lines.append(f"- {entry}")

        return "\n".join(lines)


__all__ = ["CheckSummaryPresenter", "GroupedViolationView"]
