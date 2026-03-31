from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path

from .entity import Workspace


class WorkspaceRepository(ABC):
    @abstractmethod
    def load(self, path: Path) -> Workspace:
        raise NotImplementedError


__all__ = ["WorkspaceRepository"]
