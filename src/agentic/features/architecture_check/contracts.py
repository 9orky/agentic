from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


class CheckerError(RuntimeError):
    pass


@dataclass(frozen=True)
class CheckResult:
    project_root: Path
    config_path: Path
    config_format: str
    files_found: int
    files_excluded: int
    files_checked: int
    violations: list[str]
