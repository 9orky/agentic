from __future__ import annotations

from pathlib import Path

from .app.sync_project import bootstrap_project as _bootstrap_project
from .app.sync_project import describe_workspace_contract as _describe_workspace_contract
from .app.sync_project import update_project as _update_project
from .contracts import BootstrapError, SyncResult, WorkspaceContractSummary

__all__ = ["bootstrap_project", "update_project",
           "describe_workspace_contract", "SyncResult", "WorkspaceContractSummary", "BootstrapError"]


def bootstrap_project(project_root: Path) -> SyncResult:
    return _bootstrap_project(project_root)


def update_project(project_root: Path) -> SyncResult:
    return _update_project(project_root)


def describe_workspace_contract(project_root: Path) -> WorkspaceContractSummary:
    return _describe_workspace_contract(project_root)
