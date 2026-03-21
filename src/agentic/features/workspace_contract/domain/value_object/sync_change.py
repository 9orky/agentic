from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .shared_rule_path import SharedRulePath
from .sync_action import SyncAction
from .workspace_contract_layout import WorkspaceContractLayout


@dataclass(frozen=True)
class SyncChange:
    shared_rule_path: SharedRulePath
    action: SyncAction

    def destination_path(self, project_root: Path, layout: WorkspaceContractLayout) -> Path:
        return layout.shared_rule_destination(project_root, self.shared_rule_path)
