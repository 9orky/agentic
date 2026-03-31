from __future__ import annotations

from pathlib import Path


class SyncReportBuilder:
    def build_sync_result(
        self,
        target_dir: Path,
        created_dir: bool,
        created_files: tuple[Path, ...],
        updated_files: tuple[Path, ...],
        preserved_files: tuple[Path, ...],
    ) -> dict[str, object]:
        return {
            "target_dir": target_dir,
            "created_dir": created_dir,
            "created_files": tuple(
                sorted(created_files, key=lambda path: path.as_posix())
            ),
            "updated_files": tuple(
                sorted(updated_files, key=lambda path: path.as_posix())
            ),
            "preserved_files": tuple(
                sorted(preserved_files, key=lambda path: path.as_posix())
            ),
        }
