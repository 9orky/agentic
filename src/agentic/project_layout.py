from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class AgenticProjectLayout:
    agentic_dir_names: tuple[str, ...] = ("agentic", ".agentic")
    config_file_stem: str = "agentic"
    config_extensions: tuple[str, ...] = (".yaml", ".yml")
    bootstrap_instructions_dir_name: str = ".github"
    bootstrap_instructions_file_name: str = "copilot-instructions.md"

    def target_dir_candidates(self, project_root: Path) -> tuple[Path, ...]:
        return tuple(project_root / dir_name for dir_name in self.agentic_dir_names)

    def managed_target_dirs(self, project_root: Path) -> tuple[Path, ...]:
        existing_dirs = tuple(
            path for path in self.target_dir_candidates(project_root) if path.is_dir()
        )
        if len(existing_dirs) > 1:
            labels = ", ".join(path.name for path in existing_dirs)
            raise ValueError(
                f"Found multiple agentic directories: {labels}. Delete one of them and rerun agentic."
            )
        if existing_dirs:
            return existing_dirs
        return self.target_dir_candidates(project_root)

    def target_dir(self, project_root: Path) -> Path:
        return self.managed_target_dirs(project_root)[0]

    def config_path(self, project_root: Path, suffix: str | None = None) -> Path:
        return self.target_dir(project_root) / self.config_file_name(suffix)

    def root_config_path(self, project_root: Path, suffix: str | None = None) -> Path:
        return project_root / self.config_file_name(suffix)

    def config_file_name(self, suffix: str | None = None) -> str:
        active_suffix = suffix or self.config_extensions[0]
        return f"{self.config_file_stem}{active_suffix}"

    def config_candidate_paths(self, project_root: Path) -> tuple[Path, ...]:
        managed_paths = tuple(
            target_dir / self.config_file_name(suffix)
            for target_dir in self.managed_target_dirs(project_root)
            for suffix in self.config_extensions
        )
        root_paths = tuple(
            self.root_config_path(project_root, suffix)
            for suffix in self.config_extensions
        )
        return managed_paths + root_paths

    def config_candidate_labels(self) -> tuple[str, ...]:
        managed_labels = tuple(
            f"{dir_name}/{self.config_file_name(suffix)}"
            for dir_name in self.agentic_dir_names
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
