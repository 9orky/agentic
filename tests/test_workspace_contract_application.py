from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from agentic.features.workspace_contract.contract.application import BootstrapProject, DescribeRuleSchemaDrift, DescribeWorkspaceContract, UpdateProject


class WorkspaceContractApplicationTests(unittest.TestCase):
    def test_bootstrap_creates_runtime_files_and_preserves_report_shape(self) -> None:
        with TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)

            result = BootstrapProject().execute(project_root)

            self.assertTrue(result["created_dir"])
            self.assertEqual(result["target_dir"], project_root / "agentic")
            self.assertIn(project_root / "agentic" /
                          "agentic.yaml", result["created_files"])
            self.assertIn(project_root / ".github" /
                          "copilot-instructions.md", result["created_files"])
            self.assertIn(project_root / "agentic" / "rules" /
                          "AGENT.md", result["created_files"])
            self.assertEqual(result["updated_files"], ())

    def test_update_only_marks_changed_shared_docs_as_updated(self) -> None:
        with TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)

            BootstrapProject().execute(project_root)
            shared_doc_path = project_root / "agentic" / "rules" / "AGENT.md"
            config_path = project_root / "agentic" / "agentic.yaml"
            bootstrap_instruction_path = project_root / \
                ".github" / "copilot-instructions.md"
            shared_doc_path.write_text("locally modified\n", encoding="utf-8")
            config_path.write_text("language: php\n", encoding="utf-8")
            bootstrap_instruction_path.write_text("junk\n", encoding="utf-8")

            result = UpdateProject().execute(project_root)

            self.assertIn(shared_doc_path, result["updated_files"])
            self.assertIn(bootstrap_instruction_path, result["updated_files"])
            self.assertIn(config_path, result["preserved_files"])
            self.assertNotIn(shared_doc_path, result["preserved_files"])

    def test_describe_reports_present_missing_and_local_extension_paths(self) -> None:
        with TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)

            BootstrapProject().execute(project_root)
            existing_shared_doc_path = project_root / "agentic" / "rules" / "AGENT.md"
            missing_shared_doc_path = project_root / \
                "agentic" / "rules" / "planning" / "PLANNING.md"
            missing_shared_doc_path.unlink()
            override_path = project_root / "agentic" / "rules" / "overrides" / "TESTS.md"
            project_specific_path = project_root / "agentic" / \
                "rules" / "project-specific" / "LOCAL.md"
            override_path.write_text("override\n", encoding="utf-8")
            project_specific_path.write_text("local\n", encoding="utf-8")

            summary = DescribeWorkspaceContract().execute(project_root)

            self.assertTrue(summary.agentic_dir_exists)
            self.assertTrue(summary.config_exists)
            self.assertIn(existing_shared_doc_path, summary.shared_rule_paths)
            self.assertIn(missing_shared_doc_path,
                          summary.missing_shared_rule_paths)
            self.assertEqual(summary.override_paths, (override_path,))
            self.assertEqual(summary.project_specific_paths,
                             (project_specific_path,))


class RuleSchemaValidationApplicationTests(unittest.TestCase):
    def test_reports_no_drift_for_packaged_rules_and_bootstrapped_local_mirror(self) -> None:
        with TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)

            BootstrapProject().execute(project_root)

            result = DescribeRuleSchemaDrift().execute(project_root)

            self.assertFalse(result.has_findings)
            self.assertIn(Path("AGENT.md"), result.packaged_documents)
            self.assertIn(Path("feature") / "module" / "layers" /
                          "APPLICATION.md", result.local_documents)

    def test_reports_anchor_drift_in_local_mirror(self) -> None:
        with TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)

            BootstrapProject().execute(project_root)
            local_application_doc = (
                project_root
                / "agentic"
                / "rules"
                / "feature"
                / "module"
                / "layers"
                / "APPLICATION.md"
            )
            local_application_doc.write_text(
                local_application_doc.read_text(encoding="utf-8").replace(
                    "### Required Anchors",
                    "### Required Anchor Set",
                ),
                encoding="utf-8",
            )

            result = DescribeRuleSchemaDrift().execute(project_root)

            self.assertTrue(result.has_findings)
            self.assertEqual(result.findings[0].scope, "local")
            self.assertEqual(result.findings[0].document_path, Path(
                "feature") / "module" / "layers" / "APPLICATION.md")
            self.assertEqual(result.findings[0].code, "anchor-profile-drift")
            self.assertIsNone(result.findings[0].section_heading)

    def test_reports_missing_managed_document_in_local_mirror(self) -> None:
        with TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)

            BootstrapProject().execute(project_root)
            missing_local_doc = project_root / "agentic" / \
                "rules" / "planning" / "PLANNING.md"
            missing_local_doc.unlink()

            result = DescribeRuleSchemaDrift().execute(project_root)

            self.assertTrue(result.has_findings)
            self.assertEqual(result.findings[0].scope, "local")
            self.assertEqual(result.findings[0].document_path, Path(
                "planning") / "PLANNING.md")
            self.assertEqual(result.findings[0].code, "missing-local-document")
            self.assertIsNone(result.findings[0].section_heading)

    def test_can_exclude_local_mirror_validation(self) -> None:
        with TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)

            BootstrapProject().execute(project_root)
            local_agent_doc = project_root / "agentic" / "rules" / "AGENT.md"
            local_agent_doc.write_text("broken\n", encoding="utf-8")

            result = DescribeRuleSchemaDrift().execute(
                project_root, include_local_mirror=False)

            self.assertFalse(result.has_findings)
            self.assertEqual(result.local_documents, ())


if __name__ == "__main__":
    unittest.main()
