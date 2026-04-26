from __future__ import annotations

from dataclasses import dataclass

from .value_object import ReadingPriority, RiskFinding, SummarySection


@dataclass(frozen=True)
class ArchitectureSummaryReport:
    sections: tuple[SummarySection, ...]
    reading_priorities: tuple[ReadingPriority, ...] = ()
    risk_findings: tuple[RiskFinding, ...] = ()


__all__ = ["ArchitectureSummaryReport"]
