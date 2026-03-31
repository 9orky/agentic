from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class SharedRulePath:
    relative_path: Path

    def __post_init__(self) -> None:
        normalized_path = Path(*self.relative_path.parts)
        if normalized_path.is_absolute():
            raise ValueError("Shared rule paths must be relative")
        if not normalized_path.parts:
            raise ValueError("Shared rule paths must not be empty")
        if ".." in normalized_path.parts:
            raise ValueError(
                "Shared rule paths must not escape the rules tree")
        if normalized_path.parts[0] == "rules":
            raise ValueError(
                "Shared rule paths are relative to the rules tree")
        if normalized_path.parts[0] in {"overrides", "project-specific"}:
            raise ValueError(
                "Shared rule paths must not point at repo-local extension directories")
        object.__setattr__(self, "relative_path", normalized_path)

    def as_posix(self) -> str:
        return self.relative_path.as_posix()

    def rules_relative_path(self) -> Path:
        return Path("rules") / self.relative_path
