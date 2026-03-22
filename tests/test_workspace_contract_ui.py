from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

import click

from agentic.features.workspace_contract import BootstrapError, RuleSchemaValidationResult, SyncResult, bootstrap_project, describe_rule_schema_drift, describe_workspace_contract, update_project
from agentic.features.workspace_contract.cli import workspace_contract_cli
from agentic.features.workspace_contract.contract.ui.views import RuleSchemaDriftView, SyncSummaryView


class WorkspaceContractBoundaryTests(unittest.TestCase):
    def test_feature_boundary_preserves_sync_contract_shape(self) -> None:
        with TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)

            bootstrap_result = bootstrap_project(project_root)
            update_result = update_project(project_root)
            summary = describe_workspace_contract(project_root)
            drift_result = describe_rule_schema_drift(project_root)

            self.assertIsInstance(bootstrap_result, SyncResult)
            self.assertIsInstance(update_result, SyncResult)
            self.assertTrue(summary.config_exists)
            self.assertIsInstance(drift_result, RuleSchemaValidationResult)

    def test_feature_boundary_raises_bootstrap_error_for_invalid_target(self) -> None:
        with TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            (project_root / "agentic").write_text("not a directory\n", encoding="utf-8")

            with self.assertRaises(BootstrapError):
                bootstrap_project(project_root)


class WorkspaceContractUiTests(unittest.TestCase):
    def test_cli_init_renders_created_files_and_next_step(self) -> None:
        app = click.Group()
        workspace_contract_cli(app)

        with TemporaryDirectory() as temp_dir:
            output = StringIO()
            with redirect_stdout(output):
                exit_code = app.main(
                    ["init", "--project-root", temp_dir], standalone_mode=False)

            self.assertEqual(exit_code, 0)
            rendered = output.getvalue()
            self.assertIn("Created agentic.", rendered)
            self.assertIn("Created ", rendered)
            self.assertIn("agentic/agentic.yaml", rendered)
            self.assertIn(".github/copilot-instructions.md", rendered)
            self.assertIn("agentic check", rendered)

    def test_cli_update_renders_updated_shared_files(self) -> None:
        app = click.Group()
        workspace_contract_cli(app)

        with TemporaryDirectory() as temp_dir:
            bootstrap_project(Path(temp_dir))
            shared_doc_path = Path(temp_dir) / "agentic" / "rules" / "AGENT.md"
            shared_doc_path.write_text("locally modified\n", encoding="utf-8")

            output = StringIO()
            with redirect_stdout(output):
                exit_code = app.main(
                    ["update", "--project-root", temp_dir], standalone_mode=False)

            self.assertEqual(exit_code, 0)
            rendered = output.getvalue()
            self.assertIn("Updated 1 shared file(s).", rendered)
            self.assertIn("agentic/rules/AGENT.md", rendered)

    def test_cli_check_rules_reports_success_for_clean_workspace(self) -> None:
        app = click.Group()
        workspace_contract_cli(app)

        with TemporaryDirectory() as temp_dir:
            bootstrap_project(Path(temp_dir))

            output = StringIO()
            with redirect_stdout(output):
                exit_code = app.main(
                    ["check-rules", "--project-root", temp_dir], standalone_mode=False)

            self.assertEqual(exit_code, 0)
            rendered = output.getvalue()
            self.assertIn("Rule schema check passed", rendered)
            self.assertIn("Packaged rule documents checked:", rendered)
            self.assertIn("Local rule documents checked:", rendered)

    def test_cli_check_rules_reports_drift_and_returns_non_zero(self) -> None:
        app = click.Group()
        workspace_contract_cli(app)

        with TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            bootstrap_project(project_root)
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

            output = StringIO()
            with redirect_stdout(output):
                exit_code = app.main(
                    ["check-rules", "--project-root", temp_dir], standalone_mode=False)

            self.assertEqual(exit_code, 1)
            rendered = output.getvalue()
            self.assertIn("Rule schema drift detected.", rendered)
            self.assertIn(
                "[local] feature/module/layers/APPLICATION.md", rendered)
            self.assertIn("anchor-profile-drift", rendered)

    def test_sync_summary_view_renders_summary_counts(self) -> None:
        with TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            bootstrap_project(project_root)
            summary = describe_workspace_contract(project_root)

            rendered_lines = SyncSummaryView().render_workspace_contract_summary(
                summary, project_root=project_root)

            self.assertIn("Workspace contract at agentic.", rendered_lines)
            self.assertTrue(any(line.startswith("Shared files present: ")
                            for line in rendered_lines))
            self.assertTrue(any(line.startswith("Config present: yes")
                            for line in rendered_lines))

    def test_rule_schema_drift_view_renders_success_summary(self) -> None:
        rendered_lines = RuleSchemaDriftView().render(
            RuleSchemaValidationResult(
                packaged_documents=(Path("AGENT.md"),),
                local_documents=(Path("AGENT.md"),),
            ),
            project_root=Path("/tmp/project"),
            include_local_mirror=True,
        )

        self.assertEqual(
            rendered_lines,
            (
                "Rule schema check passed for packaged rules and local mirror.",
                "Packaged rule documents checked: 1.",
                "Local rule documents checked: 1.",
            ),
        )


if __name__ == "__main__":
    unittest.main()
