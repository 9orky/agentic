from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class AgenticProjectLayout:
    agentic_dir_name: str = "agentic"
    config_file_stem: str = "agentic"
    config_extensions: tuple[str, ...] = (".yaml", ".yml")
    bootstrap_instructions_dir_name: str = ".github"
    bootstrap_instructions_file_name: str = "copilot-instructions.md"

    def target_dir(self, project_root: Path) -> Path:
        return project_root / self.agentic_dir_name

    def config_path(self, project_root: Path, suffix: str | None = None) -> Path:
        return self.target_dir(project_root) / self.config_file_name(suffix)

    def root_config_path(self, project_root: Path, suffix: str | None = None) -> Path:
        return project_root / self.config_file_name(suffix)

    def config_file_name(self, suffix: str | None = None) -> str:
        active_suffix = suffix or self.config_extensions[0]
        return f"{self.config_file_stem}{active_suffix}"

    def config_candidate_paths(self, project_root: Path) -> tuple[Path, ...]:
        managed_paths = tuple(
            self.config_path(project_root, suffix)
            for suffix in self.config_extensions
        )
        root_paths = tuple(
            self.root_config_path(project_root, suffix)
            for suffix in self.config_extensions
        )
        return managed_paths + root_paths

    def config_candidate_labels(self) -> tuple[str, ...]:
        managed_labels = tuple(
            f"{self.agentic_dir_name}/{self.config_file_name(suffix)}"
            for suffix in self.config_extensions
        )
        root_labels = tuple(
            self.config_file_name(suffix)
            for suffix in self.config_extensions
        )
        return managed_labels + root_labels

    def bootstrap_instruction_path(self, project_root: Path) -> Path:
        return (
            project_root
            / self.bootstrap_instructions_dir_name
            / self.bootstrap_instructions_file_name
        )
