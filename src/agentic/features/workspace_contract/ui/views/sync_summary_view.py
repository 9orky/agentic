from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path
from typing import Any

from ..services import ProjectPathPresenter


class SyncSummaryView:
    def __init__(self, *, path_presenter: ProjectPathPresenter | None = None) -> None:
        self._path_presenter = path_presenter or ProjectPathPresenter()

    def render_bootstrap_result(self, result: Mapping[str, Any], *, project_root: Path) -> tuple[str, ...]:
        lines = list(self._render_sync_header(result, project_root=project_root))
        lines.extend(self._render_sync_details(result, project_root=project_root, include_updates=False))
        lines.append("Safe to rerun: plain 'agentic' preserves existing local files.")
        lines.append("Next step: review agentic/agentic.yaml and run 'agentic check'.")
        return tuple(lines)

    def render_update_result(self, result: Mapping[str, Any], *, project_root: Path) -> tuple[str, ...]:
        lines = list(self._render_sync_header(result, project_root=project_root))
        lines.extend(self._render_sync_details(result, project_root=project_root, include_updates=True))
        lines.append("Next step: review refreshed rules and run 'agentic check'.")
        return tuple(lines)

    def render_workspace_contract_summary(self, summary: Any, *, project_root: Path) -> tuple[str, ...]:
        lines = [
            f"Workspace contract at {self._path_presenter.present(summary.target_dir, project_root=project_root)}.",
            f"Shared files present: {len(summary.shared_rule_paths)}.",
            f"Shared files missing: {len(summary.missing_shared_rule_paths)}.",
            f"Override files: {len(summary.override_paths)}.",
            f"Project-specific files: {len(summary.project_specific_paths)}.",
            f"Config present: {'yes' if summary.config_exists else 'no'}.",
        ]
        return tuple(lines)

    def _render_sync_header(self, result: Mapping[str, Any], *, project_root: Path) -> tuple[str, ...]:
        status = "Created" if result["created_dir"] else "Found"
        rendered_target_dir = self._path_presenter.present(result["target_dir"], project_root=project_root)
        return (f"{status} {rendered_target_dir}.",)

    def _render_sync_details(
        self,
        result: Mapping[str, Any],
        *,
        project_root: Path,
        include_updates: bool,
    ) -> tuple[str, ...]:
        lines: list[str] = []
        if result["created_files"]:
            lines.append(f"Created {len(result['created_files'])} file(s).")
            lines.extend(self._render_path_list(result["created_files"], project_root=project_root))
        if include_updates and result["updated_files"]:
            lines.append(f"Updated {len(result['updated_files'])} shared file(s).")
            lines.extend(self._render_path_list(result["updated_files"], project_root=project_root))
        if result["preserved_files"]:
            lines.append(f"Preserved {len(result['preserved_files'])} existing file(s).")
        return tuple(lines)

    def _render_path_list(self, paths: tuple[Path, ...], *, project_root: Path) -> tuple[str, ...]:
        return tuple(
            f"- {self._path_presenter.present(path, project_root=project_root)}"
            for path in paths
        )