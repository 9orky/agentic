from __future__ import annotations

from pathlib import Path

from ...domain import SyncPolicy, WorkspaceContractSummary
from ...infrastructure import PackagedRulesReader, WorkspaceReader


class WorkspaceContractSummaryService:
    def __init__(
        self,
        *,
        policy: SyncPolicy,
        packaged_rules_reader: PackagedRulesReader,
        workspace_reader: WorkspaceReader,
    ) -> None:
        self._policy = policy
        self._packaged_rules_reader = packaged_rules_reader
        self._workspace_reader = workspace_reader

    def describe(self, project_root: Path) -> WorkspaceContractSummary:
        shared_rule_paths = self._packaged_rules_reader.iter_shared_rule_paths()
        existing_shared_rule_paths = self._workspace_reader.existing_shared_rule_paths(
            project_root,
            shared_rule_paths,
        )
        return self._policy.summarize_workspace_contract(
            project_root,
            shared_rule_paths,
            existing_shared_rule_paths,
            self._workspace_reader.list_override_paths(project_root),
            self._workspace_reader.list_project_specific_paths(project_root),
            agentic_dir_exists=self._workspace_reader.agentic_dir_exists(
                project_root),
            config_exists=self._workspace_reader.config_exists(project_root),
        )


def build_default_workspace_contract_summary_service() -> WorkspaceContractSummaryService:
    policy = SyncPolicy()
    return WorkspaceContractSummaryService(
        policy=policy,
        packaged_rules_reader=PackagedRulesReader(),
        workspace_reader=WorkspaceReader(layout=policy.layout),
    )
