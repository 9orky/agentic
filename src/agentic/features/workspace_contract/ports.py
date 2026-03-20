from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol


@dataclass(frozen=True)
class ResourceDocument:
    relative_path: Path
    text: str


class WorkspaceFilesystem(Protocol):
    def ensure_agentic_directory(self, project_root: Path) -> tuple[Path, bool]:
        ...

    def ensure_directory(self, path: Path) -> None:
        ...

    def path_exists(self, path: Path) -> bool:
        ...

    def write_text(self, path: Path, text: str) -> None:
        ...


class WorkspaceResources(Protocol):
    def iter_shared_documents(self) -> Iterable[ResourceDocument]:
        ...

    def default_config_text(self) -> str:
        ...
