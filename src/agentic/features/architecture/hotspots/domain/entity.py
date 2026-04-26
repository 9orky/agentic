from __future__ import annotations

from dataclasses import dataclass

from .value_object import (
    FileImportHotspotEntry,
    FileImportHotspotsSortBy,
    HotspotExplanation,
    HotspotScore,
)


@dataclass(frozen=True)
class FileImportHotspotsResult:
    entries: tuple[FileImportHotspotEntry, ...]
    sort_by: FileImportHotspotsSortBy
    descending: bool

    def to_json_dict(self) -> dict[str, object]:
        return {
            "entries": [
                {
                    "path": entry.path,
                    "imports_count": entry.imports_count,
                    "imported_by_count": entry.imported_by_count,
                    "symbol_count": entry.symbol_count,
                    "public_symbol_count": entry.public_symbol_count,
                    "line_count": entry.line_count,
                    "risk_score": entry.risk_score,
                    "dominant_signals": list(entry.dominant_signals),
                }
                for entry in self.entries
            ],
            "sort_by": self.sort_by,
            "descending": self.descending,
        }


@dataclass(frozen=True)
class SemanticHotspotReport:
    path: str
    score: HotspotScore
    explanation: HotspotExplanation

    def to_json_dict(self) -> dict[str, object]:
        return {
            "path": self.path,
            "score": {
                "total": self.score.total,
                "signals": [
                    {
                        "name": signal.name,
                        "value": signal.value,
                        "weight": signal.weight,
                        "weighted_value": signal.weighted_value,
                    }
                    for signal in self.score.signals
                ],
            },
            "explanation": {
                "summary": self.explanation.summary,
                "dominant_signals": list(self.explanation.dominant_signals),
            },
        }


__all__ = ["FileImportHotspotsResult", "SemanticHotspotReport"]
