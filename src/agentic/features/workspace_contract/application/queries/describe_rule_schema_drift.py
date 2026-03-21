from __future__ import annotations

from pathlib import Path

from ...domain import RuleSchemaPolicy, WorkspaceContractLayout
from ...infrastructure import PackagedRulesReader, RuleMarkdownParser, RuleTreeReader, WorkspaceReader
from ...infrastructure import RuleMarkdownDocument
from ..services import RuleSchemaDriftFinding, RuleSchemaReportBuilder, RuleSchemaValidationResult


class DescribeRuleSchemaDrift:
    def __init__(
        self,
        *,
        policy: RuleSchemaPolicy | None = None,
        layout: WorkspaceContractLayout | None = None,
        packaged_rules_reader: PackagedRulesReader | None = None,
        parser: RuleMarkdownParser | None = None,
        report_builder: RuleSchemaReportBuilder | None = None,
        rule_tree_reader: RuleTreeReader | None = None,
        workspace_reader: WorkspaceReader | None = None,
    ) -> None:
        active_workspace_reader = workspace_reader or WorkspaceReader()
        self._policy = policy or RuleSchemaPolicy()
        self._layout = layout or WorkspaceContractLayout()
        self._packaged_rules_reader = packaged_rules_reader or PackagedRulesReader()
        self._parser = parser or RuleMarkdownParser()
        self._report_builder = report_builder or RuleSchemaReportBuilder()
        self._rule_tree_reader = rule_tree_reader or RuleTreeReader(
            packaged_rules_reader=self._packaged_rules_reader,
            workspace_reader=active_workspace_reader,
        )
        self._workspace_reader = active_workspace_reader

    def execute(
        self,
        project_root: Path,
        *,
        include_local_mirror: bool = True,
    ) -> RuleSchemaValidationResult:
        packaged_documents = self._rule_tree_reader.iter_packaged_rule_documents()
        packaged_rule_documents = self._parsed_packaged_documents(
            packaged_documents)
        findings = list(self._validate_packaged_documents(
            packaged_rule_documents))
        local_documents: tuple[Path, ...] = ()

        if include_local_mirror:
            local_documents = tuple(
                path.relative_to(self._layout.rules_dir(project_root))
                for path in self._rule_tree_reader.iter_local_rule_documents(project_root)
            )
            findings.extend(
                self._missing_local_document_findings(
                    packaged_rule_documents=packaged_rule_documents,
                    local_documents=local_documents,
                )
            )
            findings.extend(
                self._validate_local_documents(
                    project_root,
                    local_documents,
                    packaged_rule_documents,
                )
            )

        return self._report_builder.build_validation_result(
            packaged_documents=packaged_documents,
            local_documents=local_documents,
            findings=tuple(findings),
        )

    def _validate_packaged_documents(
        self,
        packaged_rule_documents: dict[Path, RuleMarkdownDocument],
    ) -> tuple[RuleSchemaDriftFinding, ...]:
        findings: list[RuleSchemaDriftFinding] = []
        for document_path, parsed_document in packaged_rule_documents.items():
            findings.extend(
                self._validate_document_shell(
                    parsed_document,
                    document_path,
                    scope="packaged",
                )
            )
        return tuple(findings)

    def _validate_local_documents(
        self,
        project_root: Path,
        document_paths: tuple[Path, ...],
        packaged_rule_documents: dict[Path, RuleMarkdownDocument],
    ) -> tuple[RuleSchemaDriftFinding, ...]:
        findings: list[RuleSchemaDriftFinding] = []
        for relative_path in document_paths:
            parsed_document = self._parse_local_document(
                project_root, relative_path)
            findings.extend(
                self._validate_document_shell(
                    parsed_document,
                    relative_path,
                    scope="local",
                )
            )

            packaged_document = packaged_rule_documents.get(relative_path)
            if packaged_document is None:
                findings.append(
                    RuleSchemaDriftFinding(
                        scope="local",
                        document_path=relative_path,
                        document_class=parsed_document.document_class,
                        code="unexpected-document",
                        message="Document does not exist in the packaged source of truth",
                    )
                )
                continue

            findings.extend(
                self._profile_drift_findings(
                    packaged_document=packaged_document,
                    local_document=parsed_document,
                    document_path=relative_path,
                )
            )
        return tuple(findings)

    def _validate_document_shell(
        self,
        parsed_document: RuleMarkdownDocument,
        document_path: Path,
        *,
        scope: str,
    ) -> tuple[RuleSchemaDriftFinding, ...]:
        violations = self._policy.validate_document(
            document_class=parsed_document.document_class,
            observed_section_headings=parsed_document.section_headings,
            has_navigation_targets=parsed_document.has_navigation_targets,
        )

        return tuple(
            RuleSchemaDriftFinding(
                scope=scope,
                document_path=document_path,
                document_class=parsed_document.document_class,
                code=violation.code,
                message=violation.message,
                section_heading=violation.section_heading,
            )
            for violation in violations
        )

    def _parsed_packaged_documents(self, document_paths: tuple[Path, ...]) -> dict[Path, RuleMarkdownDocument]:
        return {
            document_path: self._parse_packaged_document(document_path)
            for document_path in document_paths
        }

    def _missing_local_document_findings(
        self,
        *,
        packaged_rule_documents: dict[Path, RuleMarkdownDocument],
        local_documents: tuple[Path, ...],
    ) -> tuple[RuleSchemaDriftFinding, ...]:
        local_document_set = set(local_documents)
        return tuple(
            RuleSchemaDriftFinding(
                scope="local",
                document_path=document_path,
                document_class=packaged_document.document_class,
                code="missing-local-document",
                message="Managed document is missing from the local rules mirror",
            )
            for document_path, packaged_document in packaged_rule_documents.items()
            if document_path not in local_document_set
        )

    def _parse_packaged_document(self, document_path: Path) -> RuleMarkdownDocument:
        return self._parser.parse(
            self._packaged_rules_reader.read_rule_document_text(document_path),
            source_path=document_path,
        )

    def _parse_local_document(
        self,
        project_root: Path,
        relative_path: Path,
    ) -> RuleMarkdownDocument:
        absolute_path = self._layout.rules_dir(project_root) / relative_path
        return self._parser.parse(
            self._workspace_reader.read_text(absolute_path),
            source_path=relative_path,
        )

    def _profile_drift_findings(
        self,
        *,
        packaged_document: RuleMarkdownDocument,
        local_document: RuleMarkdownDocument,
        document_path: Path,
    ) -> tuple[RuleSchemaDriftFinding, ...]:
        findings: list[RuleSchemaDriftFinding] = []

        if local_document.document_class is not packaged_document.document_class:
            findings.append(
                RuleSchemaDriftFinding(
                    scope="local",
                    document_path=document_path,
                    document_class=local_document.document_class,
                    code="document-class-drift",
                    message=(
                        "Document class differs from the packaged source of truth: "
                        f"expected {packaged_document.document_class.value}, got {local_document.document_class.value}"
                    ),
                )
            )

        if local_document.section_headings != packaged_document.section_headings:
            findings.append(
                RuleSchemaDriftFinding(
                    scope="local",
                    document_path=document_path,
                    document_class=local_document.document_class,
                    code="section-profile-drift",
                    message="Section headings differ from the packaged source of truth",
                )
            )

        if local_document.anchor_headings != packaged_document.anchor_headings:
            findings.append(
                RuleSchemaDriftFinding(
                    scope="local",
                    document_path=document_path,
                    document_class=local_document.document_class,
                    code="anchor-profile-drift",
                    message="Anchor headings differ from the packaged source of truth",
                )
            )

        if local_document.navigation_targets != packaged_document.navigation_targets:
            findings.append(
                RuleSchemaDriftFinding(
                    scope="local",
                    document_path=document_path,
                    document_class=local_document.document_class,
                    code="navigation-target-drift",
                    message="Navigation targets differ from the packaged source of truth",
                )
            )

        return tuple(findings)
