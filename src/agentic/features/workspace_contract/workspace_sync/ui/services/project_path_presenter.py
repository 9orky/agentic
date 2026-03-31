from __future__ import annotations

from pathlib import Path


class ProjectPathPresenter:
    def present(self, path: Path, *, project_root: Path) -> str:
        try:
            return path.relative_to(project_root).as_posix()
        except ValueError:
            return str(path)
