from __future__ import annotations

from pathlib import Path

from ....domain import SyncPolicy
from ....infrastructure import PackagedRulesReader, WorkspaceReader, WorkspaceWriter
from .sync_report_builder import SyncReportBuilder


class WorkspaceContractSyncService:
    def __init__(
        self,
        *,
        policy: SyncPolicy,
        packaged_rules_reader: PackagedRulesReader,
        workspace_reader: WorkspaceReader,
        workspace_writer: WorkspaceWriter,
        sync_report_builder: SyncReportBuilder,
    ) -> None:
        self._policy = policy
        self._packaged_rules_reader = packaged_rules_reader
        self._workspace_reader = workspace_reader
        self._workspace_writer = workspace_writer
        self._sync_report_builder = sync_report_builder

    def bootstrap(self, project_root: Path) -> dict[str, object]:
        return self._sync_report_builder.build_sync_result(
            *self._sync_project(project_root, overwrite_existing_shared_docs=False)
        )

    def update(self, project_root: Path) -> dict[str, object]:
        return self._sync_report_builder.build_sync_result(
            *self._sync_project(project_root, overwrite_existing_shared_docs=True)
        )

    def _sync_project(
        self,
        project_root: Path,
        *,
        overwrite_existing_shared_docs: bool,
    ) -> tuple[Path, bool, tuple[Path, ...], tuple[Path, ...], tuple[Path, ...]]:
        target_dir, created_dir = self._workspace_writer.ensure_target_directory(
            project_root)
        self._workspace_writer.ensure_local_extension_directories(project_root)

        shared_rule_paths = self._packaged_rules_reader.iter_shared_rule_paths()
        existing_shared_rule_paths = self._workspace_reader.existing_shared_rule_paths(
            project_root,
            shared_rule_paths,
        )
        planned_changes = self._policy.plan_shared_rule_changes(
            project_root,
            shared_rule_paths,
            existing_shared_rule_paths,
            overwrite_existing_shared_docs=overwrite_existing_shared_docs,
        )

        created_files: list[Path] = []
        updated_files: list[Path] = []
        preserved_files: list[Path] = []

        for change in planned_changes:
            destination_path = change.destination_path(
                project_root, self._policy.layout)
            document_text = self._packaged_rules_reader.read_document_text(
                change.shared_rule_path)
            if change.action == change.action.CREATE:
                self._workspace_writer.write_text(
                    destination_path, document_text)
                created_files.append(destination_path)
                continue

            if change.action == change.action.PRESERVE:
                preserved_files.append(destination_path)
                continue

            if self._workspace_reader.read_text(destination_path) == document_text:
                preserved_files.append(destination_path)
                continue

            self._workspace_writer.write_text(destination_path, document_text)
            updated_files.append(destination_path)

        config_path = self._policy.layout.config_path(project_root)
        if self._workspace_reader.path_exists(config_path):
            preserved_files.append(config_path)
        else:
            self._workspace_writer.write_text(
                config_path,
                self._packaged_rules_reader.default_config_text(),
            )
            created_files.append(config_path)

        bootstrap_instruction_path = self._policy.layout.bootstrap_instruction_path(
            project_root)
        bootstrap_instruction_text = self._packaged_rules_reader.default_bootstrap_instruction_text()
        if self._workspace_reader.path_exists(bootstrap_instruction_path):
            if (
                overwrite_existing_shared_docs
                and self._workspace_reader.read_text(bootstrap_instruction_path) != bootstrap_instruction_text
            ):
                self._workspace_writer.write_text(
                    bootstrap_instruction_path,
                    bootstrap_instruction_text,
                )
                updated_files.append(bootstrap_instruction_path)
            else:
                preserved_files.append(bootstrap_instruction_path)
        else:
            self._workspace_writer.write_text(
                bootstrap_instruction_path,
                bootstrap_instruction_text,
            )
            created_files.append(bootstrap_instruction_path)

        return (
            target_dir,
            created_dir,
            tuple(created_files),
            tuple(updated_files),
            tuple(preserved_files),
        )


def build_default_workspace_contract_sync_service() -> WorkspaceContractSyncService:
    policy = SyncPolicy()
    return WorkspaceContractSyncService(
        policy=policy,
        packaged_rules_reader=PackagedRulesReader(),
        workspace_reader=WorkspaceReader(layout=policy.layout),
        workspace_writer=WorkspaceWriter(layout=policy.layout),
        sync_report_builder=SyncReportBuilder(),
    )
