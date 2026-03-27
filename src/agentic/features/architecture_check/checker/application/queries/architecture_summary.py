from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ArchitectureSummary:
    project_root: Path
    config_path: Path
    config_format: str
    language: str
    runtime_command: str
    files_found: int = 0
    files_excluded: int = 0
    files_checked: int = 0
    violations: tuple[str, ...] = ()
    check_error: str | None = None


__all__ = ["ArchitectureSummary"]
