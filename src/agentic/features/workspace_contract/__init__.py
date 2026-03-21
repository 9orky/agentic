from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from .application import BootstrapProject as _BootstrapProject
from .application import DescribeWorkspaceContract as _DescribeWorkspaceContract
from .application import UpdateProject as _UpdateProject
from .domain import WorkspaceContractSummary


class BootstrapError(RuntimeError):
    pass


@dataclass
class SyncResult:
    target_dir: Path
    created_dir: bool = False
    created_files: list[Path] = field(default_factory=list)
    updated_files: list[Path] = field(default_factory=list)
    preserved_files: list[Path] = field(default_factory=list)


__all__ = [
    "BootstrapError",
    "SyncResult",
    "WorkspaceContractSummary",
    "bootstrap_project",
    "describe_workspace_contract",
    "update_project",
]


def bootstrap_project(project_root: Path) -> SyncResult:
    return _coerce_sync_result(_run_sync_command(_BootstrapProject(), project_root))


def update_project(project_root: Path) -> SyncResult:
    return _coerce_sync_result(_run_sync_command(_UpdateProject(), project_root))


def describe_workspace_contract(project_root: Path) -> WorkspaceContractSummary:
    try:
        return _DescribeWorkspaceContract().execute(project_root)
    except NotADirectoryError as exc:
        raise BootstrapError(str(exc)) from exc


def _run_sync_command(command, project_root: Path) -> dict[str, object]:
    try:
        return command.execute(project_root)
    except NotADirectoryError as exc:
        raise BootstrapError(str(exc)) from exc


def _coerce_sync_result(result: dict[str, object]) -> SyncResult:
    return SyncResult(
        target_dir=result["target_dir"],
        created_dir=bool(result["created_dir"]),
        created_files=list(result["created_files"]),
        updated_files=list(result["updated_files"]),
        preserved_files=list(result["preserved_files"]),
    )