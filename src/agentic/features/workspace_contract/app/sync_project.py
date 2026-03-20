from __future__ import annotations

from pathlib import Path

from ..adapters.filesystem import LocalWorkspaceFilesystem
from ..adapters.resources import PackagedWorkspaceResources
from ..contracts import SyncResult
from ..domain.sync_policy import CONFIG_FILE_NAME, PROJECT_SPECIFIC_DIRECTORY
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

    local_filesystem.ensure_directory(target_dir / PROJECT_SPECIFIC_DIRECTORY)

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
