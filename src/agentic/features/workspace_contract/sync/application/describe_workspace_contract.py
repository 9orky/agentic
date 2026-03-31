from __future__ import annotations

from pathlib import Path

from ..domain import WorkspaceContractSummary, WorkspaceRepository
from ..infrastructure import file_repository


def describe_workspace_contract(
    project_root: Path,
    *,
    repository: WorkspaceRepository = file_repository,
) -> WorkspaceContractSummary:
    return repository.load(project_root).summarize()


__all__ = ["describe_workspace_contract"]
