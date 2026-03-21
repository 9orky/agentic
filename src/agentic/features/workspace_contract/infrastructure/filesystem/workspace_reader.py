from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path

from ...domain import SharedRulePath, WorkspaceContractLayout


class WorkspaceReader:
    def agentic_dir_exists(
        self,
        project_root: Path,
        *,
        layout: WorkspaceContractLayout | None = None,
    ) -> bool:
        active_layout = layout or WorkspaceContractLayout()
        return active_layout.target_dir(project_root).is_dir()

    def config_exists(
        self,
        project_root: Path,
        *,
        layout: WorkspaceContractLayout | None = None,
    ) -> bool:
        active_layout = layout or WorkspaceContractLayout()
        return active_layout.config_path(project_root).exists()

    def existing_shared_rule_paths(
        self,
        project_root: Path,
        shared_rule_paths: Iterable[SharedRulePath],
        *,
        layout: WorkspaceContractLayout | None = None,
    ) -> tuple[Path, ...]:
        active_layout = layout or WorkspaceContractLayout()
        return tuple(
            sorted(
                (
                    active_layout.shared_rule_destination(project_root, shared_rule_path)
                    for shared_rule_path in shared_rule_paths
                    if active_layout.shared_rule_destination(project_root, shared_rule_path).exists()
                ),
                key=lambda path: path.as_posix(),
            )
        )

    def path_exists(self, path: Path) -> bool:
        return path.exists()

    def read_text(self, path: Path) -> str:
        return path.read_text(encoding="utf-8")

    def list_override_paths(
        self,
        project_root: Path,
        *,
        layout: WorkspaceContractLayout | None = None,
    ) -> tuple[Path, ...]:
        active_layout = layout or WorkspaceContractLayout()
        return self._list_files(active_layout.overrides_dir(project_root))

    def list_project_specific_paths(
        self,
        project_root: Path,
        *,
        layout: WorkspaceContractLayout | None = None,
    ) -> tuple[Path, ...]:
        active_layout = layout or WorkspaceContractLayout()
        return self._list_files(active_layout.project_specific_dir(project_root))

    def _list_files(self, directory: Path) -> tuple[Path, ...]:
        if not directory.is_dir():
            return ()

        return tuple(sorted((path for path in directory.rglob("*") if path.is_file()), key=lambda path: path.as_posix()))