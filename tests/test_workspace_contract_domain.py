from pathlib import Path
import unittest

from agentic.features.workspace_contract.contract.domain import RuleDocumentClass, RuleDocumentSchema, RuleSchemaPolicy, SharedRulePath, SyncAction, SyncPolicy, WorkspaceContractLayout


class SharedRulePathTests(unittest.TestCase):
    def test_rejects_non_shared_rule_locations(self) -> None:
        with self.assertRaises(ValueError):
            SharedRulePath(Path("rules") / "AGENT.md")

        with self.assertRaises(ValueError):
            SharedRulePath(Path("overrides") / "LOCAL.md")

        with self.assertRaises(ValueError):
            SharedRulePath(Path("..") / "AGENT.md")

    def test_returns_rules_relative_path(self) -> None:
        shared_rule_path = SharedRulePath(Path("feature") / "FEATURE.md")

        self.assertEqual(shared_rule_path.rules_relative_path(),
                         Path("rules") / "feature" / "FEATURE.md")


class WorkspaceContractLayoutTests(unittest.TestCase):
    def test_resolves_runtime_paths(self) -> None:
        project_root = Path("/tmp/project")
        layout = WorkspaceContractLayout()
        shared_rule_path = SharedRulePath(Path("AGENT.md"))

        self.assertEqual(layout.target_dir(project_root),
                         project_root / "agentic")
        self.assertEqual(layout.rules_dir(project_root),
                         project_root / "agentic" / "rules")
        self.assertEqual(layout.overrides_dir(project_root),
                         project_root / "agentic" / "rules" / "overrides")
        self.assertEqual(layout.project_specific_dir(
            project_root), project_root / "agentic" / "rules" / "project-specific")
        self.assertEqual(layout.config_path(project_root),
                         project_root / "agentic" / "agentic.yaml")
        self.assertEqual(
            layout.bootstrap_instruction_path(project_root),
            project_root / ".github" / "copilot-instructions.md",
        )
        self.assertEqual(
            layout.shared_rule_destination(project_root, shared_rule_path),
            project_root / "agentic" / "rules" / "AGENT.md",
        )


class SyncPolicyTests(unittest.TestCase):
    def test_bootstrap_plan_creates_or_preserves_shared_docs(self) -> None:
        project_root = Path("/tmp/project")
        policy = SyncPolicy()
        shared_rule_paths = [
            SharedRulePath(Path("feature") / "FEATURE.md"),
            SharedRulePath(Path("AGENT.md")),
        ]
        existing_paths = [project_root / "agentic" / "rules" / "AGENT.md"]

        changes = policy.plan_shared_rule_changes(
            project_root,
            shared_rule_paths,
            existing_paths,
            overwrite_existing_shared_docs=False,
        )

        self.assertEqual([change.shared_rule_path.as_posix()
                         for change in changes], ["AGENT.md", "feature/FEATURE.md"])
        self.assertEqual([change.action for change in changes], [
                         SyncAction.PRESERVE, SyncAction.CREATE])

    def test_update_plan_marks_existing_shared_docs_for_update(self) -> None:
        project_root = Path("/tmp/project")
        policy = SyncPolicy()
        shared_rule_paths = [SharedRulePath(Path("AGENT.md"))]
        existing_paths = [project_root / "agentic" / "rules" / "AGENT.md"]

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
            SharedRulePath(Path("AGENT.md")),
            SharedRulePath(Path("planning") / "PLANNING.md"),
        ]
        existing_shared_rule_paths = [
            project_root / "agentic" / "rules" / "AGENT.md"]
        override_paths = [project_root / "agentic" /
                          "rules" / "overrides" / "TESTS.md"]
        project_specific_paths = [
            project_root / "agentic" / "rules" / "project-specific" / "LOCAL.md"]

        summary = policy.summarize_workspace_contract(
            project_root,
            shared_rule_paths,
            existing_shared_rule_paths,
            override_paths,
            project_specific_paths,
            agentic_dir_exists=True,
            config_exists=False,
        )

        self.assertTrue(summary.agentic_dir_exists)
        self.assertFalse(summary.config_exists)
        self.assertEqual(summary.target_dir, project_root / "agentic")
        self.assertEqual(summary.config_path, project_root /
                         "agentic" / "agentic.yaml")
        self.assertEqual(summary.shared_rule_paths,
                         (project_root / "agentic" / "rules" / "AGENT.md",))
        self.assertEqual(
            summary.missing_shared_rule_paths,
            (project_root / "agentic" / "rules" / "planning" / "PLANNING.md",),
        )
        self.assertEqual(summary.override_paths, tuple(override_paths))
        self.assertEqual(summary.project_specific_paths,
                         tuple(project_specific_paths))


class RuleDocumentSchemaTests(unittest.TestCase):
    def test_navigational_schema_exposes_expected_required_sections(self) -> None:
        schema = RuleDocumentSchema.navigational()

        self.assertEqual(schema.document_class, RuleDocumentClass.NAVIGATIONAL)
        self.assertEqual(
            tuple(
                requirement.canonical_heading for requirement in schema.required_sections()),
            ("Purpose", "Use This When", "Available Options",
             "Navigation Rule", "Exit Condition"),
        )
        self.assertTrue(schema.navigation_targets_required)

    def test_leaf_schema_supports_scope_as_ownership_alias(self) -> None:
        schema = RuleDocumentSchema.leaf()

        self.assertEqual(schema.document_class, RuleDocumentClass.LEAF)
        ownership_requirement = schema.required_sections()[2]
        self.assertTrue(ownership_requirement.matches("Ownership"))
        self.assertTrue(ownership_requirement.matches("Scope"))
        self.assertFalse(schema.navigation_targets_required)


class RuleSchemaPolicyTests(unittest.TestCase):
    def test_validates_navigational_document_with_required_sections(self) -> None:
        violations = RuleSchemaPolicy().validate_document(
            document_class=RuleDocumentClass.NAVIGATIONAL,
            observed_section_headings=(
                "Purpose",
                "Use This When",
                "Available Options",
                "Navigation Rule",
                "Local Context",
                "Exit Condition",
            ),
            has_navigation_targets=True,
        )

        self.assertEqual(violations, ())

    def test_reports_missing_required_leaf_section(self) -> None:
        violations = RuleSchemaPolicy().validate_document(
            document_class=RuleDocumentClass.LEAF,
            observed_section_headings=(
                "Purpose",
                "Applies When",
                "Scope",
                "Constraints",
                "Acceptance Check",
            ),
            has_navigation_targets=False,
        )

        self.assertEqual([violation.code for violation in violations], [
                         "missing-section"])
        self.assertEqual(violations[0].section_heading, "Core Rules")

    def test_reports_invalid_required_section_order(self) -> None:
        violations = RuleSchemaPolicy().validate_document(
            document_class=RuleDocumentClass.LEAF,
            observed_section_headings=(
                "Purpose",
                "Applies When",
                "Scope",
                "Constraints",
                "Core Rules",
                "Acceptance Check",
            ),
            has_navigation_targets=False,
        )

        self.assertEqual([violation.code for violation in violations], [
                         "invalid-section-order"])
        self.assertEqual(
            violations[0].message,
            "Section order is invalid: Constraints appears before Core Rules",
        )

    def test_reports_missing_navigation_targets_only_for_navigational_documents(self) -> None:
        policy = RuleSchemaPolicy()

        navigational_violations = policy.validate_document(
            document_class=RuleDocumentClass.NAVIGATIONAL,
            observed_section_headings=(
                "Purpose",
                "Use This When",
                "Available Options",
                "Navigation Rule",
                "Exit Condition",
            ),
            has_navigation_targets=False,
        )
        leaf_violations = policy.validate_document(
            document_class=RuleDocumentClass.LEAF,
            observed_section_headings=(
                "Purpose",
                "Applies When",
                "Ownership",
                "Core Rules",
                "Constraints",
                "Acceptance Check",
            ),
            has_navigation_targets=False,
        )

        self.assertEqual(
            [violation.code for violation in navigational_violations],
            ["missing-navigation-targets"],
        )
        self.assertEqual(leaf_violations, ())


if __name__ == "__main__":
    unittest.main()
