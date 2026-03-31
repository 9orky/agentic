import agentic.features.workspace_contract as workspace_contract_boundary
import agentic.features.workspace_contract.rules.ui as rules_ui
import agentic.features.workspace_contract.rules.ui.views as rules_ui_views
import agentic.features.workspace_contract.workspace_sync.ui as workspace_sync_ui
import agentic.features.workspace_contract.workspace_sync.ui.services as workspace_sync_ui_services
import agentic.features.workspace_contract.workspace_sync.ui.views as workspace_sync_ui_views
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

import click

from agentic.features.workspace_contract import BootstrapError, RuleSchemaReport, SyncResult, bootstrap_project, build_rule_schema_report, describe_workspace_contract, update_project
from agentic.features.workspace_contract.cli import workspace_contract_cli
from agentic.features.workspace_contract.rules.application import RuleDocumentReport, RuleSchemaViolationReport
from agentic.features.workspace_contract.rules.ui.views import RuleSchemaReportView, build_default_rule_schema_report_view
from agentic.features.workspace_contract.workspace_sync.ui import ProjectPathPresenter
from agentic.features.workspace_contract.workspace_sync.ui.views import SyncSummaryView, build_default_sync_summary_view


class WorkspaceContractBoundaryTests(unittest.TestCase):
    def test_feature_boundary_exports_expected_public_seam(self) -> None:
        self.assertEqual(
            workspace_contract_boundary.__all__,
            [
                "BootstrapError",
                "RuleDocumentReport",
                "RuleSchemaReport",
                "RuleSchemaViolationReport",
                "SyncResult",
                "WorkspaceContractSummary",
                "bootstrap_project",
                "build_rule_schema_report",
                "describe_workspace_contract",
                "update_project",
            ],
        )

    def test_feature_boundary_preserves_sync_contract_shape(self) -> None:
        with TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)

            bootstrap_result = bootstrap_project(project_root)
            update_result = update_project(project_root)
            summary = describe_workspace_contract(project_root)
            report = build_rule_schema_report()

            self.assertIsInstance(bootstrap_result, SyncResult)
            self.assertIsInstance(update_result, SyncResult)
            self.assertTrue(summary.config_exists)
            self.assertIsInstance(report, RuleSchemaReport)

    def test_feature_boundary_raises_bootstrap_error_for_invalid_target(self) -> None:
        with TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            (project_root / "agentic").write_text("not a directory\n", encoding="utf-8")

            with self.assertRaises(BootstrapError):
                bootstrap_project(project_root)


class WorkspaceContractUiTests(unittest.TestCase):
    def test_sync_ui_package_exports_expected_public_seam(self) -> None:
        self.assertEqual(
            workspace_sync_ui.__all__,
            ["ProjectPathPresenter", "SyncSummaryView",
                "build_default_sync_summary_view"],
        )

    def test_rules_ui_package_exports_expected_public_seam(self) -> None:
        self.assertEqual(
            rules_ui.__all__,
            ["RuleSchemaReportView", "build_default_rule_schema_report_view", "rule_schema_cli"],
        )

    def test_ui_service_and_view_packages_export_expected_public_seams(self) -> None:
        self.assertEqual(
            workspace_sync_ui_services.__all__,
            ["ProjectPathPresenter"],
        )
        self.assertEqual(
            workspace_sync_ui_views.__all__,
            [
                "SyncSummaryView",
                "build_default_sync_summary_view",
            ],
        )
        self.assertEqual(
            rules_ui_views.__all__,
            [
                "RuleSchemaReportView",
                "build_default_rule_schema_report_view",
            ],
        )

    def test_ui_directory_matches_allowed_anchor_shape(self) -> None:
        ui_dir = Path(workspace_sync_ui.__file__).resolve().parent
        entries = {
            path.name
            for path in ui_dir.iterdir()
            if path.name != "__pycache__"
        }

        self.assertEqual(entries, {"__init__.py", "services", "views"})

        rules_ui_dir = Path(rules_ui.__file__).resolve().parent
        rules_entries = {
            path.name
            for path in rules_ui_dir.iterdir()
            if path.name != "__pycache__"
        }

        self.assertEqual(rules_entries, {"__init__.py", "cli.py", "views.py"})

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
            shared_doc_path = Path(temp_dir) / "agentic" / "rules" / "INDEX.md"
            shared_doc_path.write_text("locally modified\n", encoding="utf-8")

            output = StringIO()
            with redirect_stdout(output):
                exit_code = app.main(
                    ["update", "--project-root", temp_dir], standalone_mode=False)

            self.assertEqual(exit_code, 0)
            rendered = output.getvalue()
            self.assertIn("Updated 1 shared file(s).", rendered)
            self.assertIn("agentic/rules/INDEX.md", rendered)

    def test_cli_check_rules_reports_success_for_clean_workspace(self) -> None:
        app = click.Group()
        workspace_contract_cli(app)

        output = StringIO()
        with redirect_stdout(output):
            exit_code = app.main(["check-rules"], standalone_mode=False)

        self.assertEqual(exit_code, 0)
        rendered = output.getvalue()
        self.assertIn("Rule schema report.", rendered)
        self.assertIn("Documents checked:", rendered)
        self.assertIn("Documents with issues: 0.", rendered)

    def test_sync_summary_view_renders_summary_counts(self) -> None:
        with TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            bootstrap_project(project_root)
            summary = describe_workspace_contract(project_root)

            rendered_lines = build_default_sync_summary_view().render_workspace_contract_summary(
                summary, project_root=project_root)

            self.assertIn("Workspace contract at agentic.", rendered_lines)
            self.assertTrue(any(line.startswith("Shared files present: ")
                            for line in rendered_lines))
            self.assertTrue(any(line.startswith("Config present: yes")
                            for line in rendered_lines))

    def test_rule_schema_report_view_renders_summary_and_violations(self) -> None:
        rendered_lines = build_default_rule_schema_report_view().render(
            RuleSchemaReport(
                documents=(
                    RuleDocumentReport(
                        path=Path("INDEX.md"),
                        violations=(),
                    ),
                    RuleDocumentReport(
                        path=Path("execution/STEP.md"),
                        violations=(
                            RuleSchemaViolationReport(
                                code="missing-section",
                                message="Missing required section: Handoff Checks",
                                section_heading="Handoff Checks",
                            ),
                        ),
                    ),
                ),
                documents_checked=2,
                documents_with_issues=1,
                has_findings=True,
            )
        )

        self.assertEqual(
            rendered_lines,
            (
                "Rule schema report.",
                "Documents checked: 2.",
                "Documents with issues: 1.",
                "- INDEX.md: ok",
                "- execution/STEP.md: 1 violation(s) - missing-section (Handoff Checks) - Missing required section: Handoff Checks",
            ),
        )

    def test_views_require_explicit_path_presenter(self) -> None:
        self.assertEqual(
            tuple(__import__("inspect").signature(SyncSummaryView).parameters),
            ("path_presenter",),
        )
        self.assertEqual(
            tuple(__import__("inspect").signature(RuleSchemaReportView).parameters),
            (),
        )
        presenter = ProjectPathPresenter()
        self.assertIsInstance(SyncSummaryView(
            path_presenter=presenter), SyncSummaryView)
        self.assertIsInstance(RuleSchemaReportView(), RuleSchemaReportView)


if __name__ == "__main__":
    unittest.main()
