from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel, ConfigDict

from ..domain import RuleDocumentCheck, RuleDocumentClass, RuleDocumentFile, RuleDocumentParseError, RuleSchemaPolicy
from ..infrastructure import file_repository


class RuleSchemaViolationReport(BaseModel):
    model_config = ConfigDict(frozen=True)

    code: str
    message: str
    section_heading: str | None = None


class RuleDocumentReport(BaseModel):
    model_config = ConfigDict(frozen=True)

    path: Path
    document_class: RuleDocumentClass | None = None
    observed_section_headings: tuple[str, ...] = ()
    has_navigation_targets: bool = False
    violations: tuple[RuleSchemaViolationReport, ...]
    exception: str | None = None


class RuleSchemaReport(BaseModel):
    model_config = ConfigDict(frozen=True)

    documents: tuple[RuleDocumentReport, ...]
    documents_checked: int
    documents_with_issues: int
    has_findings: bool


def build_rule_schema_report() -> RuleSchemaReport:
    policy = RuleSchemaPolicy()
    documents = tuple(
        _map_document_report(document, policy)
        for document in file_repository.find()
    )
    documents_with_issues = sum(
        1
        for document in documents
        if document.exception is not None or bool(document.violations)
    )
    return RuleSchemaReport(
        documents=documents,
        documents_checked=len(documents),
        documents_with_issues=documents_with_issues,
        has_findings=documents_with_issues > 0,
    )


def _map_document_report(
    document_file: RuleDocumentFile,
    policy: RuleSchemaPolicy,
) -> RuleDocumentReport:
    try:
        return _report_from_check(policy.inspect_document(document_file))
    except RuleDocumentParseError as exc:
        return RuleDocumentReport(
            path=document_file.path,
            violations=(),
            exception=str(exc),
        )


def _report_from_check(document_check: RuleDocumentCheck) -> RuleDocumentReport:
    document = document_check.document
    return RuleDocumentReport(
        path=document.path,
        document_class=document.document_class,
        observed_section_headings=document.observed_section_headings,
        has_navigation_targets=document.has_navigation_targets,
        violations=tuple(
            RuleSchemaViolationReport.model_validate(
                violation, from_attributes=True)
            for violation in document_check.violations
        ),
    )


__all__ = [
    "RuleDocumentReport",
    "RuleSchemaReport",
    "RuleSchemaViolationReport",
    "build_rule_schema_report",
]
