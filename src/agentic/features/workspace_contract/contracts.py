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


@dataclass(frozen=True)
class WorkspaceContractSummary:
    project_root: Path
    target_dir: Path
    agentic_dir_exists: bool
    config_path: Path
    config_exists: bool
    shared_rule_paths: tuple[Path, ...] = ()
    missing_shared_rule_paths: tuple[Path, ...] = ()
    override_paths: tuple[Path, ...] = ()
    project_specific_paths: tuple[Path, ...] = ()
    bootstrap_preserves_existing_files: bool = True
    update_overwrites_shared_docs: bool = True
    update_preserves_config: bool = True
    update_preserves_local_extensions: bool = True
