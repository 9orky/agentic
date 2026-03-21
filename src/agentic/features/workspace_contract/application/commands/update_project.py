from __future__ import annotations

from pathlib import Path

from .bootstrap_project import BootstrapProject


class UpdateProject(BootstrapProject):
    def execute(self, project_root: Path) -> dict[str, object]:
        return self._sync_report_builder.build_sync_result(
            *self._sync_project(project_root, overwrite_existing_shared_docs=True)
        )