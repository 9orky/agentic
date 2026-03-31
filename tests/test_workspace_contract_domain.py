import agentic.features.workspace_contract.rules.domain as rules_domain
import agentic.features.workspace_contract.rules.domain.service as rules_domain_service
import agentic.features.workspace_contract.rules.domain.value_object as rules_domain_value_object
import agentic.features.workspace_contract.workspace_sync.domain as workspace_sync_domain
import agentic.features.workspace_contract.workspace_sync.domain.service as workspace_sync_domain_service
import agentic.features.workspace_contract.workspace_sync.domain.value_object as workspace_sync_domain_value_object
from pathlib import Path
import unittest

from agentic.features.workspace_contract.rules.domain import RuleDocumentClass, RuleDocumentSchema, RuleSchemaPolicy
from agentic.features.workspace_contract.workspace_sync.domain import SharedRulePath, SyncAction, SyncPolicy, WorkspaceContractLayout


class WorkspaceContractDomainPackageTests(unittest.TestCase):
    def test_workspace_sync_domain_package_exports_expected_public_seam(self) -> None:
        self.assertEqual(
            workspace_sync_domain.__all__,
            [
                "SharedRulePath",
                "SyncAction",
                "SyncChange",
                "SyncPolicy",
                "WorkspaceContractLayout",
                "WorkspaceContractSummary",
            ],
        )

    def test_rules_domain_package_exports_expected_public_seam(self) -> None:
        self.assertEqual(
            rules_domain.__all__,
            [
                "RuleDocumentClass",
                "RuleDocument",
                "RuleDocumentCheck",
                "RuleDocumentFile",
                "RuleDocumentParseError",
                "RuleDocumentRepository",
                "RuleDocumentSchema",
                "RuleSchemaPolicy",
                "RuleSchemaViolation",
                "RuleSectionRequirement",
            ],
        )

    def test_domain_service_anchor_exports_expected_public_seam(self) -> None:
        self.assertEqual(
            workspace_sync_domain_service.__all__,
            ["SyncPolicy"],
        )
        self.assertEqual(
            rules_domain_service.__all__,
            ["RuleSchemaPolicy"],
        )

    def test_domain_value_object_anchor_exports_expected_public_seam(self) -> None:
        self.assertEqual(
            workspace_sync_domain_value_object.__all__,
            [
                "SharedRulePath",
                "SyncAction",
                "SyncChange",
                "WorkspaceContractLayout",
                "WorkspaceContractSummary",
            ],
        )
        self.assertEqual(
            rules_domain_value_object.__all__,
            [
                "RuleDocumentClass",
                "RuleDocumentParseError",
                "RuleSchemaViolation",
                "RuleSectionRequirement",
            ],
        )

    def test_domain_directory_matches_allowed_anchor_shape(self) -> None:
        domain_dir = Path(workspace_sync_domain.__file__).resolve().parent
        entries = {
            path.name
            for path in domain_dir.iterdir()
            if path.name != "__pycache__"
        }

        self.assertEqual(entries, {"__init__.py", "service", "value_object"})

        rules_domain_dir = Path(
            rules_domain.__file__).resolve().parent
        rules_entries = {
            path.name
            for path in rules_domain_dir.iterdir()
            if path.name != "__pycache__"
        }

        self.assertEqual(
            rules_entries,
            {"__init__.py", "entity.py", "repository.py", "service.py", "value_object.py"},
        )


class SharedRulePathTests(unittest.TestCase):
    def test_rejects_non_shared_rule_locations(self) -> None:
        with self.assertRaises(ValueError):
            SharedRulePath(Path("rules") / "INDEX.md")

        with self.assertRaises(ValueError):
            SharedRulePath(Path("overrides") / "LOCAL.md")

        with self.assertRaises(ValueError):
            SharedRulePath(Path("..") / "INDEX.md")

    def test_returns_rules_relative_path(self) -> None:
        shared_rule_path = SharedRulePath(Path("feature") / "FEATURE.md")

        self.assertEqual(shared_rule_path.rules_relative_path(),
                         Path("rules") / "feature" / "FEATURE.md")


class WorkspaceContractLayoutTests(unittest.TestCase):
    def test_resolves_runtime_paths(self) -> None:
        project_root = Path("/tmp/project")
        layout = WorkspaceContractLayout()
        shared_rule_path = SharedRulePath(Path("INDEX.md"))

        self.assertEqual(layout.target_dir(project_root),
                         project_root / "agentic")
        self.assertEqual(layout.rules_dir(project_root),
                         project_root / "agentic" / "rules")
        self.assertEqual(layout.config_path(project_root),
                         project_root / "agentic" / "agentic.yaml")
        self.assertEqual(
            layout.bootstrap_instruction_path(project_root),
            project_root / ".github" / "copilot-instructions.md",
        )
        self.assertEqual(
            layout.shared_rule_destination(project_root, shared_rule_path),
            project_root / "agentic" / "rules" / "INDEX.md",
        )


class SyncPolicyTests(unittest.TestCase):
    def test_bootstrap_plan_creates_or_preserves_shared_docs(self) -> None:
        project_root = Path("/tmp/project")
        policy = SyncPolicy()
        shared_rule_paths = [
            SharedRulePath(Path("structure") / "MODULE.md"),
            SharedRulePath(Path("INDEX.md")),
        ]
        existing_paths = [project_root / "agentic" / "rules" / "INDEX.md"]

        changes = policy.plan_shared_rule_changes(
            project_root,
            shared_rule_paths,
            existing_paths,
            overwrite_existing_shared_docs=False,
        )

        self.assertEqual([change.shared_rule_path.as_posix()
                 for change in changes], ["INDEX.md", "structure/MODULE.md"])
        self.assertEqual([change.action for change in changes], [
                         SyncAction.PRESERVE, SyncAction.CREATE])

    def test_update_plan_marks_existing_shared_docs_for_update(self) -> None:
        project_root = Path("/tmp/project")
        policy = SyncPolicy()
        shared_rule_paths = [SharedRulePath(Path("INDEX.md"))]
        existing_paths = [project_root / "agentic" / "rules" / "INDEX.md"]

        changes = policy.plan_shared_rule_changes(
            project_root,
            shared_rule_paths,
            existing_paths,
            overwrite_existing_shared_docs=True,
        )

        self.assertEqual(changes[0].action, SyncAction.UPDATE)

    def test_summary_reports_present_and_missing_shared_docs(self) -> None:
        project_root = Path("/tmp/project")
        policy = SyncPolicy()
        shared_rule_paths = [
            SharedRulePath(Path("INDEX.md")),
            SharedRulePath(Path("structure") / "MODULE.md"),
        ]
        existing_shared_rule_paths = [
            project_root / "agentic" / "rules" / "INDEX.md"]

        summary = policy.summarize_workspace_contract(
            project_root,
            shared_rule_paths,
            existing_shared_rule_paths,
            (),
            (),
            agentic_dir_exists=True,
            config_exists=False,
        )

        self.assertTrue(summary.agentic_dir_exists)
        self.assertFalse(summary.config_exists)
        self.assertEqual(summary.target_dir, project_root / "agentic")
        self.assertEqual(summary.config_path, project_root /
                         "agentic" / "agentic.yaml")
        self.assertEqual(summary.shared_rule_paths,
                         (project_root / "agentic" / "rules" / "INDEX.md",))
        self.assertEqual(
            summary.missing_shared_rule_paths,
            (project_root / "agentic" / "rules" / "structure" / "MODULE.md",),
        )
        self.assertEqual(summary.override_paths, ())
        self.assertEqual(summary.project_specific_paths, ())


class RuleDocumentSchemaTests(unittest.TestCase):
    def test_navigational_schema_exposes_expected_required_sections(self) -> None:
        schema = RuleDocumentSchema.navigational()

        self.assertEqual(schema.document_class, RuleDocumentClass.NAVIGATIONAL)
        self.assertEqual(
            tuple(
                requirement.canonical_heading for requirement in schema.required_sections()),
            ("Stop Or Descend", "Review Checks"),
        )
        self.assertTrue(schema.navigation_targets_required)

    def test_policy_schema_exposes_expected_required_sections(self) -> None:
        schema = RuleDocumentSchema.policy()

        self.assertEqual(schema.document_class, RuleDocumentClass.POLICY)
        self.assertEqual(
            tuple(
                requirement.canonical_heading for requirement in schema.required_sections()),
            ("Required Decisions", "Core Rules", "Review Checks"),
        )
        self.assertFalse(schema.navigation_targets_required)


class RuleSchemaPolicyTests(unittest.TestCase):
    def test_validates_navigational_document_with_required_sections(self) -> None:
        violations = RuleSchemaPolicy().validate_document(
            document_class=RuleDocumentClass.NAVIGATIONAL,
            observed_section_headings=(
                "Use This Branch When",
                "Stop Or Descend",
                "Review Checks",
            ),
            has_navigation_targets=True,
        )

        self.assertEqual(violations, ())

    def test_reports_missing_required_policy_section(self) -> None:
        violations = RuleSchemaPolicy().validate_document(
            document_class=RuleDocumentClass.POLICY,
            observed_section_headings=(
                "Required Decisions",
                "Review Checks",
            ),
            has_navigation_targets=False,
        )

        self.assertEqual([violation.code for violation in violations], [
                         "missing-section"])
        self.assertEqual(violations[0].section_heading, "Core Rules")

    def test_reports_invalid_required_section_order(self) -> None:
        violations = RuleSchemaPolicy().validate_document(
            document_class=RuleDocumentClass.EXECUTION,
            observed_section_headings=(
                "Required Sections",
                "Execution Rules",
                "Implementation Tree Rules",
                "Step Contract Rules",
                "Review Checks",
                "Handoff Checks",
            ),
            has_navigation_targets=False,
            stage="step",
        )

        self.assertEqual([violation.code for violation in violations], [
                         "invalid-section-order"])
        self.assertEqual(
            violations[0].message,
            "Section order is invalid: Execution Rules appears before Step Contract Rules",
        )

    def test_reports_missing_navigation_targets_only_for_navigational_documents(self) -> None:
        policy = RuleSchemaPolicy()

        navigational_violations = policy.validate_document(
            document_class=RuleDocumentClass.NAVIGATIONAL,
            observed_section_headings=(
                "Stop Or Descend",
                "Review Checks",
            ),
            has_navigation_targets=False,
        )
        policy_violations = policy.validate_document(
            document_class=RuleDocumentClass.POLICY,
            observed_section_headings=(
                "Required Decisions",
                "Core Rules",
                "Review Checks",
            ),
            has_navigation_targets=False,
        )

        self.assertEqual(
            [violation.code for violation in navigational_violations],
            ["missing-navigation-targets"],
        )
        self.assertEqual(policy_violations, ())


if __name__ == "__main__":
    unittest.main()
