from dataclasses import dataclass
from pathlib import Path

from .architecture_check_config import ArchitectureCheckConfig


@dataclass(frozen=True)
class ConfigLoadResult:
    path: Path
    config: ArchitectureCheckConfig
    source_format: str
