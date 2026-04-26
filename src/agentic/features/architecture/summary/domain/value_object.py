from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

RiskLevel = Literal["low", "medium", "high"]


@dataclass(frozen=True)
class SummarySection:
    title: str
    entries: tuple[str, ...]


@dataclass(frozen=True)
class ReadingPriority:
    path: str
    reason: str
    risk_level: RiskLevel = "medium"


@dataclass(frozen=True)
class RiskFinding:
    path: str
    summary: str
    risk_level: RiskLevel = "medium"


__all__ = ["ReadingPriority", "RiskFinding", "SummarySection"]
