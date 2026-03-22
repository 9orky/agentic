from __future__ import annotations

from pathlib import Path

from ...domain import SyncPolicy, WorkspaceContractSummary
from ...infrastructure import PackagedRulesReader, WorkspaceReader


class DescribeWorkspaceContract:
    def __init__(
        self,
        *,
        policy: SyncPolicy | None = None,
        packaged_rules_reader: PackagedRulesReader | None = None,
        workspace_reader: WorkspaceReader | None = None,
    ) -> None:
        self._policy = policy or SyncPolicy()
        self._packaged_rules_reader = packaged_rules_reader or PackagedRulesReader()
        self._workspace_reader = workspace_reader or WorkspaceReader()

    def execute(self, project_root: Path) -> WorkspaceContractSummary:
        shared_rule_paths = self._packaged_rules_reader.iter_shared_rule_paths()
        existing_shared_rule_paths = self._workspace_reader.existing_shared_rule_paths(
            project_root,
            shared_rule_paths,
            layout=self._policy.layout,
        )
        return self._policy.summarize_workspace_contract(
            project_root,
            shared_rule_paths,
            existing_shared_rule_paths,
            self._workspace_reader.list_override_paths(
                project_root, layout=self._policy.layout),
            self._workspace_reader.list_project_specific_paths(
                project_root, layout=self._policy.layout),
            agentic_dir_exists=self._workspace_reader.agentic_dir_exists(
                project_root, layout=self._policy.layout),
            config_exists=self._workspace_reader.config_exists(
                project_root, layout=self._policy.layout),
        )
