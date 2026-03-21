from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from ..resources import PackagedRulesReader
from .workspace_reader import WorkspaceReader


@dataclass(frozen=True)
class RuleTreeReader:
    packaged_rules_reader: PackagedRulesReader = field(
        default_factory=PackagedRulesReader)
    workspace_reader: WorkspaceReader = field(default_factory=WorkspaceReader)

    def iter_packaged_rule_documents(self) -> tuple[Path, ...]:
        return self.packaged_rules_reader.iter_rule_document_paths()

    def iter_local_rule_documents(self, project_root: Path) -> tuple[Path, ...]:
        return self.workspace_reader.existing_rule_document_paths(project_root)
