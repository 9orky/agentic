from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path
from typing import Any


class SyncSummaryView:
    def render_bootstrap_result(self, result: Mapping[str, Any], *, project_root: Path) -> tuple[str, ...]:
        target_dir = _present_path(
            result["target_dir"], project_root=project_root)
        lines = list(self._render_sync_header(
            result, project_root=project_root))
        lines.extend(
            self._render_sync_details(
                result,
                project_root=project_root,
                include_updates=False,
            )
        )
        lines.append(
            f"Local profile surface: {target_dir}/rules/local/.")
        lines.append(
            f"Safe to rerun: plain 'agentic' preserves existing local files in {target_dir}/rules/local/.")
        lines.append(
            f"Next step: review {target_dir}/agentic.yaml and {target_dir}/rules/local/ and run 'agentic check'.")
        return tuple(lines)

    def render_update_result(self, result: Mapping[str, Any], *, project_root: Path) -> tuple[str, ...]:
        target_dir = _present_path(
            result["target_dir"], project_root=project_root)
        lines = list(self._render_sync_header(
            result, project_root=project_root))
        lines.extend(
            self._render_sync_details(
                result,
                project_root=project_root,
                include_updates=True,
            )
        )
        lines.append(
            f"Next step: review refreshed shared rules, {target_dir}/agentic.yaml, and {target_dir}/rules/local/ and run 'agentic check'.")
        return tuple(lines)

    def _render_sync_header(self, result: Mapping[str, Any], *, project_root: Path) -> tuple[str, ...]:
        status = "Created" if result["created_dir"] else "Found"
        return (f"{status} {_present_path(result['target_dir'], project_root=project_root)}.",)

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
            lines.extend(self._render_path_list(
                result["created_files"], project_root=project_root))
        if include_updates and result["updated_files"]:
            lines.append(
                f"Updated {len(result['updated_files'])} shared file(s).")
            lines.extend(self._render_path_list(
                result["updated_files"], project_root=project_root))
        if result["preserved_files"]:
            lines.append(
                f"Preserved {len(result['preserved_files'])} existing file(s).")
        return tuple(lines)

    def _render_path_list(self, paths: tuple[Path, ...], *, project_root: Path) -> tuple[str, ...]:
        return tuple(
            f"- {_present_path(path, project_root=project_root)}"
            for path in paths
        )


def build_default_sync_summary_view() -> SyncSummaryView:
    return SyncSummaryView()


def _present_path(path: Path, *, project_root: Path) -> str:
    try:
        return path.relative_to(project_root).as_posix()
    except ValueError:
        return str(path)


__all__ = ["SyncSummaryView", "build_default_sync_summary_view"]
