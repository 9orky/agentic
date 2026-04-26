from __future__ import annotations

from typing import Protocol


class SummarySectionLike(Protocol):
    @property
    def title(self) -> str: ...

    @property
    def entries(self) -> tuple[str, ...]: ...


class ReadingPriorityLike(Protocol):
    @property
    def path(self) -> str: ...

    @property
    def reason(self) -> str: ...

    @property
    def risk_level(self) -> str: ...


class RiskFindingLike(Protocol):
    @property
    def path(self) -> str: ...

    @property
    def summary(self) -> str: ...

    @property
    def risk_level(self) -> str: ...


class ArchitectureSummaryReportLike(Protocol):
    @property
    def sections(self) -> tuple[SummarySectionLike, ...]: ...

    @property
    def reading_priorities(self) -> tuple[ReadingPriorityLike, ...]: ...

    @property
    def risk_findings(self) -> tuple[RiskFindingLike, ...]: ...


class ArchitectureSummaryView:
    def render(self, report: ArchitectureSummaryReportLike) -> str:
        lines: list[str] = ["Architecture Summary:"]

        for section in report.sections:
            lines.append("")
            lines.append(f"{section.title}:")
            for entry in section.entries:
                lines.append(f"- {entry}")

        if report.reading_priorities:
            lines.append("")
            lines.append("Suggested Reading Order:")
            for entry in report.reading_priorities:
                lines.append(f"- [{entry.risk_level}] {entry.path}: {entry.reason}")

        if report.risk_findings:
            lines.append("")
            lines.append("Risk Notes:")
            for finding in report.risk_findings:
                lines.append(f"- [{finding.risk_level}] {finding.path}: {finding.summary}")

        return "\n".join(lines)


__all__ = ["ArchitectureSummaryView"]
