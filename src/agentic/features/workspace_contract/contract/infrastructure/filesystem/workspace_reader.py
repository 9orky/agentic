from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path

from ...domain import SharedRulePath, WorkspaceContractLayout


class WorkspaceReader:
    def __init__(self, *, layout: WorkspaceContractLayout = WorkspaceContractLayout()) -> None:
        self._layout = layout

    def _resolve_layout(self, layout: WorkspaceContractLayout | None) -> WorkspaceContractLayout:
        return layout or self._layout

    def agentic_dir_exists(
        self,
        project_root: Path,
        *,
        layout: WorkspaceContractLayout | None = None,
    ) -> bool:
        resolved_layout = self._resolve_layout(layout)
        return resolved_layout.target_dir(project_root).is_dir()

    def config_exists(
        self,
        project_root: Path,
        *,
        layout: WorkspaceContractLayout | None = None,
    ) -> bool:
        resolved_layout = self._resolve_layout(layout)
        return resolved_layout.config_path(project_root).exists()

    def existing_shared_rule_paths(
        self,
        project_root: Path,
        shared_rule_paths: Iterable[SharedRulePath],
        *,
        layout: WorkspaceContractLayout | None = None,
    ) -> tuple[Path, ...]:
        resolved_layout = self._resolve_layout(layout)
        return tuple(
            sorted(
                (
                    resolved_layout.shared_rule_destination(
                        project_root, shared_rule_path)
                    for shared_rule_path in shared_rule_paths
                    if resolved_layout.shared_rule_destination(project_root, shared_rule_path).exists()
                ),
                key=lambda path: path.as_posix(),
            )
        )

    def existing_rule_document_paths(
        self,
        project_root: Path,
        *,
        layout: WorkspaceContractLayout | None = None,
    ) -> tuple[Path, ...]:
        resolved_layout = self._resolve_layout(layout)
        rules_dir = resolved_layout.rules_dir(project_root)
        if not rules_dir.is_dir():
            return ()

        ignored_directories = {
            resolved_layout.overrides_dir_name,
            resolved_layout.project_specific_dir_name,
        }

        return tuple(
            sorted(
                (
                    path
                    for path in rules_dir.rglob("*.md")
                    if path.is_file()
                    and not any(part in ignored_directories for part in path.relative_to(rules_dir).parts)
                    and not any(part.startswith(".") for part in path.relative_to(rules_dir).parts)
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
        resolved_layout = self._resolve_layout(layout)
        return self._list_files(resolved_layout.overrides_dir(project_root))

    def list_project_specific_paths(
        self,
        project_root: Path,
        *,
        layout: WorkspaceContractLayout | None = None,
    ) -> tuple[Path, ...]:
        resolved_layout = self._resolve_layout(layout)
        return self._list_files(resolved_layout.project_specific_dir(project_root))

    def _list_files(self, directory: Path) -> tuple[Path, ...]:
        if not directory.is_dir():
            return ()

        return tuple(sorted((path for path in directory.rglob("*") if path.is_file()), key=lambda path: path.as_posix()))
