from __future__ import annotations

from dataclasses import dataclass
from fnmatch import fnmatch
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


@dataclass(frozen=True)
class CodeGenerationConfig:
    skip_globs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        normalized_globs = tuple(
            value.strip().replace("\\", "/")
            for value in self.skip_globs
            if value.strip()
        )
        object.__setattr__(self, "skip_globs", normalized_globs)

    def should_skip(self, relative_path: RelativePath) -> bool:
        relative_path_text = relative_path.as_posix()
        return any(fnmatch(relative_path_text, pattern) for pattern in self.skip_globs)


__all__ = ["CodeGenerationConfig", "RelativePath"]
