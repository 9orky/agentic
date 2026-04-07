from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path

from .entity import Recipe


class RecipeRepository(ABC):
    def __init__(self, root_path: Path) -> None:
        self._root_path = Path(root_path)

    @property
    def root_path(self) -> Path:
        return self._root_path

    @abstractmethod
    def find_all(self) -> tuple[Recipe, ...]:
        raise NotImplementedError

    @abstractmethod
    def get_by_name(self, name: str) -> Recipe:
        raise NotImplementedError


__all__ = ["RecipeRepository"]
