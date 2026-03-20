from __future__ import annotations

from pathlib import Path

from ..adapters.filesystem import LocalWorkspaceFilesystem
from ..contracts import BootstrapError
from ..adapters.resources import PackagedWorkspaceResources
from ..contracts import SyncResult, WorkspaceContractSummary
from ..domain.sync_policy import CONFIG_FILE_NAME, CORE_RULE_DOCUMENTS, LOCAL_EXTENSION_DIRECTORIES
from ..ports import WorkspaceFilesystem, WorkspaceResources


def bootstrap_project(
    project_root: Path,
    *,
    filesystem: WorkspaceFilesystem | None = None,
    resources: WorkspaceResources | None = None,
) -> SyncResult:
    return _sync_project(
        project_root,
        overwrite_existing_shared_docs=False,
        filesystem=filesystem,
        resources=resources,
    )


def update_project(
    project_root: Path,
    *,
    filesystem: WorkspaceFilesystem | None = None,
    resources: WorkspaceResources | None = None,
) -> SyncResult:
    return _sync_project(
        project_root,
        overwrite_existing_shared_docs=True,
        filesystem=filesystem,
        resources=resources,
    )


def describe_workspace_contract(project_root: Path) -> WorkspaceContractSummary:
    target_dir = project_root / "agentic"
    if target_dir.exists() and not target_dir.is_dir():
        raise BootstrapError(f"{target_dir} exists but is not a directory")

    config_path = target_dir / CONFIG_FILE_NAME
    shared_rule_paths = []
    missing_shared_rule_paths = []

    for document_name in CORE_RULE_DOCUMENTS:
        document_path = target_dir / "rules" / document_name
        if document_path.exists():
            shared_rule_paths.append(document_path)
        else:
            missing_shared_rule_paths.append(document_path)

    override_paths = _list_files(target_dir / LOCAL_EXTENSION_DIRECTORIES[0])
    project_specific_paths = _list_files(
        target_dir / LOCAL_EXTENSION_DIRECTORIES[1])

    return WorkspaceContractSummary(
        project_root=project_root,
        target_dir=target_dir,
        agentic_dir_exists=target_dir.is_dir(),
        config_path=config_path,
        config_exists=config_path.exists(),
        shared_rule_paths=tuple(shared_rule_paths),
        missing_shared_rule_paths=tuple(missing_shared_rule_paths),
        override_paths=tuple(override_paths),
        project_specific_paths=tuple(project_specific_paths),
    )


def _sync_project(
    project_root: Path,
    *,
    overwrite_existing_shared_docs: bool,
    filesystem: WorkspaceFilesystem | None,
    resources: WorkspaceResources | None,
) -> SyncResult:
    local_filesystem = filesystem or LocalWorkspaceFilesystem()
    packaged_resources = resources or PackagedWorkspaceResources()

    target_dir, created_dir = local_filesystem.ensure_agentic_directory(
        project_root)
    result = SyncResult(target_dir=target_dir, created_dir=created_dir)

    for extension_directory in LOCAL_EXTENSION_DIRECTORIES:
        local_filesystem.ensure_directory(target_dir / extension_directory)

    for document in packaged_resources.iter_shared_documents():
        destination = target_dir / document.relative_path
        if local_filesystem.path_exists(destination):
            if overwrite_existing_shared_docs:
                local_filesystem.write_text(destination, document.text)
                result.updated_files.append(destination)
            else:
                result.preserved_files.append(destination)
            continue

        local_filesystem.write_text(destination, document.text)
        result.created_files.append(destination)

    config_path = target_dir / CONFIG_FILE_NAME
    if local_filesystem.path_exists(config_path):
        result.preserved_files.append(config_path)
    else:
        local_filesystem.write_text(
            config_path, packaged_resources.default_config_text())
        result.created_files.append(config_path)

    return result


def _list_files(directory: Path) -> list[Path]:
    if not directory.is_dir():
        return []

    return sorted(path for path in directory.rglob("*") if path.is_file())
