from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .value_object import RelativePath


@dataclass(frozen=True)
class Recipe:
    name: str
    root_path: Path
    relative_paths: tuple[RelativePath, ...] = ()

    def __post_init__(self) -> None:
        normalized_name = self.name.strip()
        if not normalized_name:
            raise ValueError("Recipe names must not be empty")

        name_path = Path(normalized_name)
        if len(name_path.parts) != 1 or name_path.parts[0] in {".", ".."}:
            raise ValueError("Recipe names must be a single folder name")

        object.__setattr__(self, "name", normalized_name)
        object.__setattr__(self, "root_path", Path(self.root_path))
        object.__setattr__(
            self,
            "relative_paths",
            _unique_relative_paths(tuple(self.relative_paths)),
        )

    def is_empty(self) -> bool:
        return len(self.relative_paths) == 0


def _unique_relative_paths(
    relative_paths: tuple[RelativePath, ...],
) -> tuple[RelativePath, ...]:
    return tuple(
        dict.fromkeys(
            sorted(relative_paths, key=lambda relative_path: relative_path.as_posix())
        )
    )


__all__ = ["Recipe"]
