from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .shared_rule_path import SharedRulePath


@dataclass(frozen=True)
class WorkspaceContractLayout:
    agentic_dir_name: str = "agentic"
    config_file_name: str = "agentic.yaml"
    bootstrap_instructions_dir_name: str = ".github"
    bootstrap_instructions_file_name: str = "copilot-instructions.md"
    rules_dir_name: str = "rules"
    overrides_dir_name: str = "overrides"
    project_specific_dir_name: str = "project-specific"

    def target_dir(self, project_root: Path) -> Path:
        return project_root / self.agentic_dir_name

    def rules_dir(self, project_root: Path) -> Path:
        return self.target_dir(project_root) / self.rules_dir_name

    def overrides_dir(self, project_root: Path) -> Path:
        return self.rules_dir(project_root) / self.overrides_dir_name

    def project_specific_dir(self, project_root: Path) -> Path:
        return self.rules_dir(project_root) / self.project_specific_dir_name

    def config_path(self, project_root: Path) -> Path:
        return self.target_dir(project_root) / self.config_file_name

    def bootstrap_instruction_path(self, project_root: Path) -> Path:
        return (
            project_root
            / self.bootstrap_instructions_dir_name
            / self.bootstrap_instructions_file_name
        )

    def shared_rule_destination(self, project_root: Path, shared_rule_path: SharedRulePath) -> Path:
        return self.rules_dir(project_root) / shared_rule_path.relative_path
