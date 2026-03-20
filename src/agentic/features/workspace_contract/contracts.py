from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


class BootstrapError(RuntimeError):
    pass


@dataclass
class SyncResult:
    target_dir: Path
    created_dir: bool = False
    created_files: list[Path] = field(default_factory=list)
    updated_files: list[Path] = field(default_factory=list)
    preserved_files: list[Path] = field(default_factory=list)
