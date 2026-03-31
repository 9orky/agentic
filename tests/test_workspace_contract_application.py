import agentic.features.workspace_contract.rules.application as rules_application
import agentic.features.workspace_contract.workspace_sync.application as workspace_sync_application
import agentic.features.workspace_contract.workspace_sync.application.commands as workspace_sync_application_commands
import agentic.features.workspace_contract.workspace_sync.application.queries as workspace_sync_application_queries
import agentic.features.workspace_contract.workspace_sync.application.services as workspace_sync_application_services
import inspect
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, cast
import unittest

from agentic.features.workspace_contract.rules.application import RuleSchemaReport, build_rule_schema_report
from agentic.features.workspace_contract.workspace_sync.application import BootstrapProject, DescribeWorkspaceContract, UpdateProject, build_default_bootstrap_project, build_default_describe_workspace_contract, build_default_update_project
from agentic.features.workspace_contract.workspace_sync.domain import WorkspaceContractSummary


class WorkspaceContractApplicationTests(unittest.TestCase):
    def test_workspace_sync_application_package_exports_only_public_seam(self) -> None:
        self.assertEqual(
            workspace_sync_application.__all__,
            [
                "BootstrapProject",
                "DescribeWorkspaceContract",
                "UpdateProject",
                "build_default_bootstrap_project",
                "build_default_describe_workspace_contract",
                "build_default_update_project",
            ],
        )

    def test_rules_application_package_exports_only_public_seam(self) -> None:
        self.assertEqual(
            rules_application.__all__,
            [
                "RuleDocumentReport",
                "RuleSchemaReport",
                "RuleSchemaViolationReport",
                "build_rule_schema_report",
            ],
        )

    def test_workspace_sync_commands_package_exports_only_public_seam(self) -> None:
        self.assertEqual(
            workspace_sync_application_commands.__all__,
            [
                "BootstrapProject",
                "UpdateProject",
                "build_default_bootstrap_project",
                "build_default_update_project",
            ],
        )

    def test_workspace_sync_queries_package_exports_only_public_seam(self) -> None:
        self.assertEqual(
            workspace_sync_application_queries.__all__,
            [
                "DescribeWorkspaceContract",
                "build_default_describe_workspace_contract",
            ],
        )

    def test_services_anchor_exports_no_cross_layer_surface(self) -> None:
        self.assertEqual(workspace_sync_application_services.__all__, [])

    def test_workspace_sync_application_directory_matches_allowed_anchor_shape(self) -> None:
        application_dir = Path(
            workspace_sync_application.__file__).resolve().parent
        entries = {
            path.name
            for path in application_dir.iterdir()
            if path.name != "__pycache__"
        }

        self.assertEqual(
            entries, {"__init__.py", "commands", "queries", "services"})

    def test_rules_application_directory_matches_allowed_anchor_shape(self) -> None:
        application_dir = Path(
            rules_application.__file__).resolve().parent
        entries = {
            path.name
            for path in application_dir.iterdir()
            if path.name != "__pycache__"
        }

        self.assertEqual(entries, {"__init__.py", "queries.py"})

    def test_workspace_sync_services_directory_matches_refactor_target_shape(self) -> None:
        services_dir = Path(
            workspace_sync_application.__file__).resolve().parent / "services"
        entries = {
            path.name
            for path in services_dir.iterdir()
            if path.name != "__pycache__"
        }

        self.assertEqual(
            entries,
            {
                "__init__.py",
                "workspace_contract_summary_service.py",
                "workspace_contract_sync",
            },
        )

    def test_commands_and_queries_depend_only_on_service_boundary(self) -> None:
        self.assertEqual(
            tuple(inspect.signature(BootstrapProject).parameters),
            ("sync_service",),
        )
        self.assertEqual(
            tuple(inspect.signature(UpdateProject).parameters),
            ("sync_service",),
        )
        self.assertEqual(
            tuple(inspect.signature(DescribeWorkspaceContract).parameters),
            ("summary_service",),
        )

    def test_update_project_uses_composition_instead_of_inheritance(self) -> None:
        self.assertFalse(issubclass(UpdateProject, BootstrapProject))

    def test_describe_workspace_contract_delegates_to_summary_service(self) -> None:
        class SummaryServiceStub:
            def __init__(self, summary: WorkspaceContractSummary) -> None:
                self.summary = summary
                self.calls: list[Path] = []

            def describe(self, project_root: Path) -> WorkspaceContractSummary:
                self.calls.append(project_root)
                return self.summary

        project_root = Path("/tmp/example-project")
        expected_summary = WorkspaceContractSummary(
            project_root=project_root,
            agentic_dir_exists=True,
            config_exists=True,
        )
        summary_service = SummaryServiceStub(expected_summary)

        result = DescribeWorkspaceContract(
            summary_service=cast(Any, summary_service)
        ).execute(project_root)

        self.assertIs(result, expected_summary)
        self.assertEqual(summary_service.calls, [project_root])

    def test_bootstrap_creates_runtime_files_and_preserves_report_shape(self) -> None:
        with TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)

            result = build_default_bootstrap_project().execute(project_root)

            self.assertTrue(result["created_dir"])
            self.assertEqual(result["target_dir"], project_root / "agentic")
            created_files = cast(tuple[Path, ...], result["created_files"])
            self.assertIn(project_root / "agentic" /
                          "agentic.yaml", created_files)
            self.assertIn(project_root / ".github" /
                          "copilot-instructions.md", created_files)
            self.assertIn(project_root / "agentic" / "rules" /
                          "INDEX.md", created_files)
            self.assertEqual(result["updated_files"], ())

    def test_update_only_marks_changed_shared_docs_as_updated(self) -> None:
        with TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)

            build_default_bootstrap_project().execute(project_root)
            shared_doc_path = project_root / "agentic" / "rules" / "INDEX.md"
            config_path = project_root / "agentic" / "agentic.yaml"
            bootstrap_instruction_path = project_root / \
                ".github" / "copilot-instructions.md"
            shared_doc_path.write_text("locally modified\n", encoding="utf-8")
            config_path.write_text("language: php\n", encoding="utf-8")
            bootstrap_instruction_path.write_text("junk\n", encoding="utf-8")

            result = build_default_update_project().execute(project_root)

            updated_files = cast(tuple[Path, ...], result["updated_files"])
            preserved_files = cast(tuple[Path, ...], result["preserved_files"])
            self.assertIn(shared_doc_path, updated_files)
            self.assertIn(bootstrap_instruction_path, updated_files)
            self.assertIn(config_path, preserved_files)
            self.assertNotIn(shared_doc_path, preserved_files)

    def test_describe_reports_present_and_missing_shared_rule_paths(self) -> None:
        with TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)

            build_default_bootstrap_project().execute(project_root)
            existing_shared_doc_path = project_root / "agentic" / "rules" / "INDEX.md"
            missing_shared_doc_path = project_root / \
                "agentic" / "rules" / "structure" / "MODULE.md"
            missing_shared_doc_path.unlink()

            summary = build_default_describe_workspace_contract().execute(project_root)

            self.assertTrue(summary.agentic_dir_exists)
            self.assertTrue(summary.config_exists)
            self.assertIn(existing_shared_doc_path, summary.shared_rule_paths)
            self.assertIn(missing_shared_doc_path,
                          summary.missing_shared_rule_paths)
            self.assertEqual(summary.override_paths, ())
            self.assertEqual(summary.project_specific_paths, ())


class RuleSchemaReportApplicationTests(unittest.TestCase):
    def test_build_rule_schema_report_returns_summary_for_packaged_rules(self) -> None:
        result = build_rule_schema_report()

        self.assertIsInstance(result, RuleSchemaReport)
        self.assertGreater(result.documents_checked, 0)
        self.assertEqual(result.documents_checked, len(result.documents))
        self.assertEqual(result.documents_with_issues, 0)
        self.assertFalse(result.has_findings)


if __name__ == "__main__":
    unittest.main()
