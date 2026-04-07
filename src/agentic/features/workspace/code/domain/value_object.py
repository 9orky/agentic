from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class RelativePath:
    value: Path

    def __post_init__(self) -> None:
        normalized_value = Path(self.value)
        if normalized_value.is_absolute():
            raise ValueError("Recipe paths must be relative")
        if not normalized_value.parts:
            raise ValueError("Recipe paths must not be empty")
        if any(part in {".", ".."} for part in normalized_value.parts):
            raise ValueError(
                "Recipe paths must not traverse outside the target root")

        object.__setattr__(self, "value", normalized_value)

    def as_posix(self) -> str:
        return self.value.as_posix()

    def resolve_from(self, root_path: Path) -> Path:
        return root_path / self.value


__all__ = ["RelativePath"]
