from __future__ import annotations

from pathlib import Path

from ...domain import SyncPolicy
from ...infrastructure import PackagedRulesReader, WorkspaceReader, WorkspaceWriter
from ..services import SyncReportBuilder


class BootstrapProject:
    def __init__(
        self,
        *,
        policy: SyncPolicy | None = None,
        packaged_rules_reader: PackagedRulesReader | None = None,
        workspace_reader: WorkspaceReader | None = None,
        workspace_writer: WorkspaceWriter | None = None,
        sync_report_builder: SyncReportBuilder | None = None,
    ) -> None:
        self._policy = policy or SyncPolicy()
        self._packaged_rules_reader = packaged_rules_reader or PackagedRulesReader()
        self._workspace_reader = workspace_reader or WorkspaceReader()
        self._workspace_writer = workspace_writer or WorkspaceWriter()
        self._sync_report_builder = sync_report_builder or SyncReportBuilder()

    def execute(self, project_root: Path) -> dict[str, object]:
        return self._sync_report_builder.build_sync_result(
            *self._sync_project(project_root, overwrite_existing_shared_docs=False)
        )

    def _sync_project(self, project_root: Path, *, overwrite_existing_shared_docs: bool) -> tuple[Path, bool, tuple[Path, ...], tuple[Path, ...], tuple[Path, ...]]:
        target_dir, created_dir = self._workspace_writer.ensure_target_directory(project_root, layout=self._policy.layout)
        self._workspace_writer.ensure_local_extension_directories(project_root, layout=self._policy.layout)

        shared_rule_paths = self._packaged_rules_reader.iter_shared_rule_paths()
        existing_shared_rule_paths = self._workspace_reader.existing_shared_rule_paths(
            project_root,
            shared_rule_paths,
            layout=self._policy.layout,
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
            destination_path = change.destination_path(project_root, self._policy.layout)
            document_text = self._packaged_rules_reader.read_document_text(change.shared_rule_path)
            if change.action == change.action.CREATE:
                self._workspace_writer.write_text(destination_path, document_text)
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
            self._workspace_writer.write_text(config_path, self._packaged_rules_reader.default_config_text())
            created_files.append(config_path)

        return (
            target_dir,
            created_dir,
            tuple(created_files),
            tuple(updated_files),
            tuple(preserved_files),
        )