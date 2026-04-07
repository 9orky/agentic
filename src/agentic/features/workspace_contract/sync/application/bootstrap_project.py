from __future__ import annotations

from pathlib import Path
from typing import TypedDict

from ..domain import SyncAction, SyncChange, WorkspaceRepository, WorkspaceWritePlan
from ..infrastructure import file_repository


class BootstrapProjectResult(TypedDict):
    target_dir: Path
    created_dir: bool
    created_files: tuple[Path, ...]
    updated_files: tuple[Path, ...]
    preserved_files: tuple[Path, ...]


def bootstrap_project(
    project_root: Path,
    *,
    repository: WorkspaceRepository = file_repository,
) -> BootstrapProjectResult:
    workspace = repository.load(project_root)
    return _materialize_write_plan(workspace.plan_bootstrap())


def _materialize_write_plan(write_plan: WorkspaceWritePlan) -> BootstrapProjectResult:
    created_dir = _ensure_target_dir(write_plan.target_dir)
    _ensure_required_dirs(write_plan.required_dirs)
    created_files: list[Path] = []
    updated_files: list[Path] = []
    preserved_files = list(write_plan.preserved_paths)

    for change in write_plan.changes:
        if change.action is SyncAction.CREATE:
            _write_sync_change(change)
            created_files.append(change.target_path)
            continue

        if change.action is SyncAction.UPDATE:
            if _has_same_content(change):
                preserved_files.append(change.target_path)
                continue

            _write_sync_change(change)
            updated_files.append(change.target_path)

    return {
        "target_dir": write_plan.target_dir,
        "created_dir": created_dir,
        "created_files": tuple(created_files),
        "updated_files": tuple(updated_files),
        "preserved_files": tuple(preserved_files),
    }


def _ensure_target_dir(target_dir: Path) -> bool:
    if target_dir.exists() and not target_dir.is_dir():
        raise NotADirectoryError(f"{target_dir} exists but is not a directory")

    if target_dir.is_dir():
        return False

    target_dir.mkdir(parents=True, exist_ok=True)
    return True


def _ensure_required_dirs(required_dirs: tuple[Path, ...]) -> None:
    for required_dir in required_dirs:
        required_dir.mkdir(parents=True, exist_ok=True)


def _has_same_content(change: SyncChange) -> bool:
    return change.target_path.is_file() and change.target_path.read_text(encoding="utf-8") == change.content


def _write_sync_change(change: SyncChange) -> None:
    change.target_path.parent.mkdir(parents=True, exist_ok=True)
    change.target_path.write_text(change.content, encoding="utf-8")


__all__ = ["BootstrapProjectResult", "bootstrap_project"]
