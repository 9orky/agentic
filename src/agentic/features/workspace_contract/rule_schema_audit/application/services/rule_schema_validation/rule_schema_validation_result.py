from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .rule_schema_drift_finding import RuleSchemaDriftFinding


@dataclass(frozen=True)
class RuleSchemaValidationResult:
    packaged_documents: tuple[Path, ...] = ()
    local_documents: tuple[Path, ...] = ()
    findings: tuple[RuleSchemaDriftFinding, ...] = ()

    @property
    def has_findings(self) -> bool:
        return bool(self.findings)
