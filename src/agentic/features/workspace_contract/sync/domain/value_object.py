from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path


@dataclass(frozen=True)
class SharedRulePath:
    value: Path

    def __post_init__(self) -> None:
        normalized_value = Path(self.value)
        if normalized_value.is_absolute():
            raise ValueError("Shared rule paths must be relative")
        if not normalized_value.parts:
            raise ValueError("Shared rule paths must not be empty")
        if normalized_value.parts[0] in {"rules", "overrides"}:
            raise ValueError(
                "Shared rule paths must be relative to the shared rules root")
        if any(part in {"..", "."} for part in normalized_value.parts):
            raise ValueError(
                "Shared rule paths must not traverse outside the rules root")
        object.__setattr__(self, "value", normalized_value)

    def as_posix(self) -> str:
        return self.value.as_posix()

    def rules_relative_path(self) -> Path:
        return Path("rules") / self.value


@dataclass(frozen=True)
class SharedRuleDocument:
    shared_rule_path: SharedRulePath
    content: str


class SyncAction(StrEnum):
    CREATE = "create"
    UPDATE = "update"


@dataclass(frozen=True)
class SyncChange:
    target_path: Path
    action: SyncAction
    content: str
    shared_rule_path: SharedRulePath | None = None


@dataclass(frozen=True)
class WorkspaceContractLayout:
    def target_dir(self, project_root: Path) -> Path:
        return project_root / "agentic"

    def rules_dir(self, project_root: Path) -> Path:
        return self.target_dir(project_root) / "rules"

    def local_dir(self, project_root: Path) -> Path:
        return self.rules_dir(project_root) / "local"

    def config_path(self, project_root: Path) -> Path:
        return self.target_dir(project_root) / "agentic.yaml"

    def bootstrap_instruction_path(self, project_root: Path) -> Path:
        return project_root / ".github" / "copilot-instructions.md"

    def shared_rule_destination(self, project_root: Path, shared_rule_path: SharedRulePath) -> Path:
        return self.rules_dir(project_root) / shared_rule_path.value


@dataclass(frozen=True)
class WorkspaceContractSummary:
    project_root: Path
    target_dir: Path
    config_path: Path
    agentic_dir_exists: bool
    config_exists: bool
    shared_rule_paths: tuple[Path, ...] = ()
    missing_shared_rule_paths: tuple[Path, ...] = ()
    local_paths: tuple[Path, ...] = ()


@dataclass(frozen=True)
class WorkspaceWritePlan:
    target_dir: Path
    required_dirs: tuple[Path, ...] = ()
    changes: tuple[SyncChange, ...] = ()
    preserved_paths: tuple[Path, ...] = ()


__all__ = [
    "SharedRuleDocument",
    "SharedRulePath",
    "SyncAction",
    "SyncChange",
    "WorkspaceContractLayout",
    "WorkspaceContractSummary",
    "WorkspaceWritePlan",
]
