from __future__ import annotations

from pathlib import Path
from ..services.workspace_contract_sync import (
    WorkspaceContractSyncService,
    build_default_workspace_contract_sync_service,
)


class UpdateProject:
    def __init__(
        self,
        *,
        sync_service: WorkspaceContractSyncService,
    ) -> None:
        self._sync_service = sync_service

    def execute(self, project_root: Path) -> dict[str, object]:
        return self._sync_service.update(project_root)


def build_default_update_project() -> UpdateProject:
    return UpdateProject(
        sync_service=build_default_workspace_contract_sync_service(),
    )
