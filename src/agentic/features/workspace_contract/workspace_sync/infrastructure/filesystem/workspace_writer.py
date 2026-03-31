from __future__ import annotations

from pathlib import Path

from ...domain import WorkspaceContractLayout


class WorkspaceWriter:
    def __init__(self, *, layout: WorkspaceContractLayout = WorkspaceContractLayout()) -> None:
        self._layout = layout

    def _resolve_layout(self, layout: WorkspaceContractLayout | None) -> WorkspaceContractLayout:
        return layout or self._layout

    def ensure_target_directory(
        self,
        project_root: Path,
        *,
        layout: WorkspaceContractLayout | None = None,
    ) -> tuple[Path, bool]:
        resolved_layout = self._resolve_layout(layout)
        target_dir = resolved_layout.target_dir(project_root)
        if target_dir.exists() and not target_dir.is_dir():
            raise NotADirectoryError(
                f"{target_dir} exists but is not a directory")

        created_dir = False
        if not target_dir.exists():
            target_dir.mkdir(parents=True, exist_ok=True)
            created_dir = True

        return target_dir, created_dir

    def ensure_local_extension_directories(
        self,
        project_root: Path,
        *,
        layout: WorkspaceContractLayout | None = None,
    ) -> tuple[Path, Path]:
        resolved_layout = self._resolve_layout(layout)
        overrides_dir = resolved_layout.overrides_dir(project_root)
        project_specific_dir = resolved_layout.project_specific_dir(
            project_root)
        self.ensure_directory(overrides_dir)
        self.ensure_directory(project_specific_dir)
        return overrides_dir, project_specific_dir

    def ensure_directory(self, path: Path) -> None:
        path.mkdir(parents=True, exist_ok=True)

    def write_text(self, path: Path, text: str) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
