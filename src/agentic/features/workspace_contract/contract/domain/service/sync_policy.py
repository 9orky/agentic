from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass, field
from pathlib import Path

from ..value_object import SharedRulePath, SyncAction, SyncChange, WorkspaceContractLayout, WorkspaceContractSummary


@dataclass(frozen=True)
class SyncPolicy:
    layout: WorkspaceContractLayout = field(default_factory=WorkspaceContractLayout)

    def expected_shared_rule_paths(
        self,
        project_root: Path,
        shared_rule_paths: Iterable[SharedRulePath],
    ) -> tuple[Path, ...]:
        return tuple(
            self.layout.shared_rule_destination(project_root, shared_rule_path)
            for shared_rule_path in self._sorted_shared_rule_paths(shared_rule_paths)
        )

    def plan_shared_rule_changes(
        self,
        project_root: Path,
        shared_rule_paths: Iterable[SharedRulePath],
        existing_shared_rule_paths: Iterable[Path],
        *,
        overwrite_existing_shared_docs: bool,
    ) -> tuple[SyncChange, ...]:
        existing_paths = {path for path in existing_shared_rule_paths}
        planned_changes = []

        for shared_rule_path in self._sorted_shared_rule_paths(shared_rule_paths):
            destination_path = self.layout.shared_rule_destination(project_root, shared_rule_path)
            if destination_path in existing_paths:
                action = SyncAction.UPDATE if overwrite_existing_shared_docs else SyncAction.PRESERVE
            else:
                action = SyncAction.CREATE
            planned_changes.append(SyncChange(shared_rule_path=shared_rule_path, action=action))

        return tuple(planned_changes)

    def summarize_workspace_contract(
        self,
        project_root: Path,
        shared_rule_paths: Iterable[SharedRulePath],
        existing_shared_rule_paths: Iterable[Path],
        override_paths: Iterable[Path],
        project_specific_paths: Iterable[Path],
        *,
        agentic_dir_exists: bool,
        config_exists: bool,
    ) -> WorkspaceContractSummary:
        expected_paths = self.expected_shared_rule_paths(project_root, shared_rule_paths)
        existing_path_set = {path for path in existing_shared_rule_paths}
        present_paths = tuple(path for path in expected_paths if path in existing_path_set)
        missing_paths = tuple(path for path in expected_paths if path not in existing_path_set)

        return WorkspaceContractSummary(
            project_root=project_root,
            agentic_dir_exists=agentic_dir_exists,
            config_exists=config_exists,
            shared_rule_paths=present_paths,
            missing_shared_rule_paths=missing_paths,
            override_paths=tuple(override_paths),
            project_specific_paths=tuple(project_specific_paths),
            layout=self.layout,
        )

    @staticmethod
    def _sorted_shared_rule_paths(shared_rule_paths: Iterable[SharedRulePath]) -> tuple[SharedRulePath, ...]:
        return tuple(sorted(shared_rule_paths, key=lambda path: path.as_posix()))