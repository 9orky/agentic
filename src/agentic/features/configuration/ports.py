from __future__ import annotations

from pathlib import Path
from typing import Protocol


class ConfigPathResolver(Protocol):
    def resolve(self, project_root: Path, explicit_config_path: str | None = None) -> Path | None:
        ...


class ConfigTextReader(Protocol):
    def read_text(self, path: Path) -> str:
        ...


class ConfigMappingLoader(Protocol):
    def load_mapping(self, raw_text: str, config_path: Path) -> tuple[dict[str, object], str]:
        ...
