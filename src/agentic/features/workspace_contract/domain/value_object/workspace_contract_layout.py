from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from agentic.project_layout import AgenticProjectLayout

from .shared_rule_path import SharedRulePath


@dataclass(frozen=True)
class WorkspaceContractLayout(AgenticProjectLayout):
    rules_dir_name: str = "rules"
    overrides_dir_name: str = "overrides"
    project_specific_dir_name: str = "project-specific"

    def rules_dir(self, project_root: Path) -> Path:
        return self.target_dir(project_root) / self.rules_dir_name

    def overrides_dir(self, project_root: Path) -> Path:
        return self.rules_dir(project_root) / self.overrides_dir_name

    def project_specific_dir(self, project_root: Path) -> Path:
        return self.rules_dir(project_root) / self.project_specific_dir_name

    def shared_rule_destination(self, project_root: Path, shared_rule_path: SharedRulePath) -> Path:
        return self.rules_dir(project_root) / shared_rule_path.relative_path
