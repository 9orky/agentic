from __future__ import annotations

from pathlib import Path

from .rule_schema_drift_finding import RuleSchemaDriftFinding
from .rule_schema_validation_result import RuleSchemaValidationResult


class RuleSchemaReportBuilder:
    def build_validation_result(
        self,
        *,
        packaged_documents: tuple[Path, ...],
        local_documents: tuple[Path, ...],
        findings: tuple[RuleSchemaDriftFinding, ...],
    ) -> RuleSchemaValidationResult:
        sorted_findings = tuple(
            sorted(
                findings,
                key=lambda finding: (
                    finding.scope,
                    finding.document_path.as_posix(),
                    finding.code,
                    finding.section_heading or "",
                ),
            )
        )
        return RuleSchemaValidationResult(
            packaged_documents=tuple(
                sorted(packaged_documents, key=lambda path: path.as_posix())),
            local_documents=tuple(
                sorted(local_documents, key=lambda path: path.as_posix())),
            findings=sorted_findings,
        )
