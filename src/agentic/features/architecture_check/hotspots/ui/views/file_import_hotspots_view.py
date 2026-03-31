from __future__ import annotations

from ...application import FileImportHotspotsResult


class FileImportHotspotsView:
    def render(self, result: FileImportHotspotsResult) -> str:
        lines = [
            "File Import Hotspots:",
            f"- Sort by: {result.sort_by}",
            f"- Order: {'desc' if result.descending else 'asc'}",
        ]

        if not result.entries:
            lines.append("- No tracked files found.")
            return "\n".join(lines)

        lines.append("")
        lines.append("Imported By  Imports  Path")
        for entry in result.entries:
            lines.append(
                f"{entry.imported_by_count:11}  {entry.imports_count:7}  {entry.path}"
            )

        return "\n".join(lines)


__all__ = ["FileImportHotspotsView"]
