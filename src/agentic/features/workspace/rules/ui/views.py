from __future__ import annotations

from ..application import RuleDocumentReport, RuleSchemaReport, RuleSchemaViolationReport


class RuleSchemaReportView:
    def render(self, report: RuleSchemaReport) -> tuple[str, ...]:
        lines = [
            "Rule schema report.",
            f"Documents discovered: {report.documents_discovered}.",
            f"Documents checked: {report.documents_checked}.",
            f"Collection coverage: {'complete' if report.collection_complete else 'incomplete'}.",
            f"Documents with issues: {report.documents_with_issues}.",
        ]
        lines.extend(self._render_document(document)
                     for document in report.documents)
        return tuple(lines)

    def _render_document(self, document: RuleDocumentReport) -> str:
        if document.exception is not None:
            return f"- {document.path}: parse-error - {document.exception}"
        if document.violations:
            details = "; ".join(
                self._render_violation(violation) for violation in document.violations
            )
            return f"- {document.path}: {len(document.violations)} violation(s) - {details}"
        return f"- {document.path}: ok"

    @staticmethod
    def _render_violation(violation: RuleSchemaViolationReport) -> str:
        if violation.reference_path is not None:
            return (
                f"{violation.code} ({violation.reference_path}) - "
                f"{violation.message}"
            )
        if violation.section_heading is None:
            return f"{violation.code} - {violation.message}"
        return (
            f"{violation.code} ({violation.section_heading}) - "
            f"{violation.message}"
        )


def build_default_rule_schema_report_view() -> RuleSchemaReportView:
    return RuleSchemaReportView()


__all__ = ["RuleSchemaReportView", "build_default_rule_schema_report_view"]
