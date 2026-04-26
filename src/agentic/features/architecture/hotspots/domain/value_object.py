from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

FileImportHotspotsSortBy = Literal[
    "risk_score",
    "imports_count",
    "imported_by_count",
    "symbol_count",
    "public_symbol_count",
    "line_count",
]


@dataclass(frozen=True)
class FileImportHotspotEntry:
    path: str
    imports_count: int
    imported_by_count: int
    symbol_count: int = 0
    public_symbol_count: int = 0
    line_count: int = 0
    risk_score: float = 0.0
    dominant_signals: tuple[str, ...] = ()


@dataclass(frozen=True)
class HotspotSignal:
    name: str
    value: float
    weight: float = 1.0

    @property
    def weighted_value(self) -> float:
        return self.value * self.weight


@dataclass(frozen=True)
class HotspotExplanation:
    summary: str
    dominant_signals: tuple[str, ...] = ()


@dataclass(frozen=True)
class HotspotScore:
    total: float
    signals: tuple[HotspotSignal, ...] = ()


__all__ = [
    "FileImportHotspotEntry",
    "FileImportHotspotsSortBy",
    "HotspotExplanation",
    "HotspotScore",
    "HotspotSignal",
]
