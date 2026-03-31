from __future__ import annotations

from pathlib import Path

from ....workspace_sync.domain import WorkspaceContractLayout
from ....workspace_sync.infrastructure import PackagedRulesReader, WorkspaceReader


class RuleTreeReader:
    def __init__(
        self,
        *,
        packaged_rules_reader: PackagedRulesReader = PackagedRulesReader(),
        workspace_reader: WorkspaceReader = WorkspaceReader(
            layout=WorkspaceContractLayout()
        ),
    ) -> None:
        self.packaged_rules_reader = packaged_rules_reader
        self.workspace_reader = workspace_reader

    def iter_packaged_rule_documents(self) -> tuple[Path, ...]:
        return self.packaged_rules_reader.iter_rule_document_paths()

    def iter_local_rule_documents(self, project_root: Path) -> tuple[Path, ...]:
        return self.workspace_reader.existing_rule_document_paths(project_root)
