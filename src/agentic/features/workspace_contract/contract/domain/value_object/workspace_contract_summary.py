from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from .workspace_contract_layout import WorkspaceContractLayout


@dataclass(frozen=True)
class WorkspaceContractSummary:
    project_root: Path
    agentic_dir_exists: bool
    config_exists: bool
    shared_rule_paths: tuple[Path, ...] = ()
    missing_shared_rule_paths: tuple[Path, ...] = ()
    override_paths: tuple[Path, ...] = ()
    project_specific_paths: tuple[Path, ...] = ()
    bootstrap_preserves_existing_files: bool = True
    update_overwrites_shared_docs: bool = True
    update_preserves_config: bool = True
    update_preserves_local_extensions: bool = True
    layout: WorkspaceContractLayout = field(default_factory=WorkspaceContractLayout)

    def __post_init__(self) -> None:
        object.__setattr__(self, "shared_rule_paths", self._sorted_paths(self.shared_rule_paths))
        object.__setattr__(self, "missing_shared_rule_paths", self._sorted_paths(self.missing_shared_rule_paths))
        object.__setattr__(self, "override_paths", self._sorted_paths(self.override_paths))
        object.__setattr__(self, "project_specific_paths", self._sorted_paths(self.project_specific_paths))

    @property
    def target_dir(self) -> Path:
        return self.layout.target_dir(self.project_root)

    @property
    def config_path(self) -> Path:
        return self.layout.config_path(self.project_root)

    @staticmethod
    def _sorted_paths(paths: tuple[Path, ...]) -> tuple[Path, ...]:
        return tuple(sorted(paths, key=lambda path: path.as_posix()))
