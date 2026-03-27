from __future__ import annotations

from pathlib import Path

from ...application import RuleSchemaValidationResult
from ..services import ProjectPathPresenter


class RuleSchemaDriftView:
    def __init__(self, *, path_presenter: ProjectPathPresenter) -> None:
        self._path_presenter = path_presenter

    def render(
        self,
        result: RuleSchemaValidationResult,
        *,
        project_root: Path,
        include_local_mirror: bool,
    ) -> tuple[str, ...]:
        if not result.has_findings:
            scope_description = "packaged rules and local mirror" if include_local_mirror else "packaged rules"
            return (
                f"Rule schema check passed for {scope_description}.",
                f"Packaged rule documents checked: {len(result.packaged_documents)}.",
                f"Local rule documents checked: {len(result.local_documents)}.",
            )

        lines = [
            "Rule schema drift detected.",
            f"Packaged rule documents checked: {len(result.packaged_documents)}.",
            f"Local rule documents checked: {len(result.local_documents)}.",
            f"Findings: {len(result.findings)}.",
        ]
        lines.extend(
            self._render_finding(finding, project_root=project_root)
            for finding in result.findings
        )
        return tuple(lines)

    def _render_finding(self, finding, *, project_root: Path) -> str:
        return (
            f"- [{finding.scope}] "
            f"{self._path_presenter.present(finding.document_path, project_root=project_root)}: "
            f"{finding.code} - {finding.message}"
        )


def build_default_rule_schema_drift_view() -> RuleSchemaDriftView:
    return RuleSchemaDriftView(path_presenter=ProjectPathPresenter())
