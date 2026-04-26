from __future__ import annotations

from typing import Protocol


class FileImportHotspotsResultLike(Protocol):
    @property
    def entries(self) -> tuple[object, ...]: ...

    @property
    def sort_by(self) -> str: ...

    @property
    def descending(self) -> bool: ...


class FileImportHotspotsView:
    def render(self, result: FileImportHotspotsResultLike) -> str:
        lines = [
            "Architecture Hotspots:",
            f"- Sort by: {result.sort_by}",
            f"- Order: {'desc' if result.descending else 'asc'}",
        ]

        if not result.entries:
            lines.append("- No tracked files found.")
            return "\n".join(lines)

        lines.append("")
        lines.append("Risk   Imported By  Imports  Symbols  Public  Lines  Path")
        for entry in result.entries:
            lines.append(
                f"{entry.risk_score:4.1f}  {entry.imported_by_count:11}  {entry.imports_count:7}  "
                f"{entry.symbol_count:7}  {entry.public_symbol_count:6}  {entry.line_count:5}  {entry.path}"
            )

        return "\n".join(lines)


class HotspotExplanationView:
    def render(self, report) -> str:
        lines = [
            "Hotspot Explanation:",
            f"- Path: {report.path}",
            f"- Risk score: {report.score.total:.2f}",
            f"- Summary: {report.explanation.summary}",
        ]
        if report.explanation.dominant_signals:
            lines.append(
                f"- Dominant signals: {', '.join(report.explanation.dominant_signals)}"
            )
        return "\n".join(lines)


__all__ = ["FileImportHotspotsView", "HotspotExplanationView"]
