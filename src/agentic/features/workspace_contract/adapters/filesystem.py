from __future__ import annotations

from pathlib import Path

from ..contracts import BootstrapError


class LocalWorkspaceFilesystem:
    def ensure_agentic_directory(self, project_root: Path) -> tuple[Path, bool]:
        target_dir = project_root / "agentic"
        if target_dir.exists() and not target_dir.is_dir():
            raise BootstrapError(f"{target_dir} exists but is not a directory")

        created_dir = False
        if not target_dir.exists():
            target_dir.mkdir(parents=True, exist_ok=True)
            created_dir = True

        return target_dir, created_dir

    def ensure_directory(self, path: Path) -> None:
        path.mkdir(parents=True, exist_ok=True)

    def path_exists(self, path: Path) -> bool:
        return path.exists()

    def write_text(self, path: Path, text: str) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
