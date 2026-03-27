import agentic.features.workspace_contract.contract.application.commands as workspace_contract_application_commands
import agentic.features.workspace_contract.contract.application.queries as workspace_contract_application_queries
import agentic.features.workspace_contract.contract.application as workspace_contract_application
import inspect
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, cast
import unittest

from agentic.features.workspace_contract.contract.application import BootstrapProject, DescribeRuleSchemaDrift, DescribeWorkspaceContract, RuleSchemaValidationResult, UpdateProject, build_default_bootstrap_project, build_default_describe_rule_schema_drift, build_default_describe_workspace_contract, build_default_update_project
from agentic.features.workspace_contract.contract.domain import WorkspaceContractSummary


class WorkspaceContractApplicationTests(unittest.TestCase):
    def test_application_package_exports_only_public_seam(self) -> None:
        self.assertEqual(
            workspace_contract_application.__all__,
            [
                "BootstrapProject",
                "DescribeRuleSchemaDrift",
                "DescribeWorkspaceContract",
                "RuleSchemaValidationResult",
                "RuleSchemaValidationService",
                "UpdateProject",
                "WorkspaceContractSummaryService",
                "WorkspaceContractSyncService",
                "build_default_bootstrap_project",
                "build_default_describe_rule_schema_drift",
                "build_default_describe_workspace_contract",
                "build_default_rule_schema_validation_service",
                "build_default_update_project",
                "build_default_workspace_contract_summary_service",
                "build_default_workspace_contract_sync_service",
            ],
        )

    def test_commands_package_exports_only_public_seam(self) -> None:
        self.assertEqual(
            workspace_contract_application_commands.__all__,
            [
                "BootstrapProject",
                "UpdateProject",
                "build_default_bootstrap_project",
                "build_default_update_project",
            ],
        )

    def test_queries_package_exports_only_public_seam(self) -> None:
        self.assertEqual(
            workspace_contract_application_queries.__all__,
            [
                "DescribeRuleSchemaDrift",
                "DescribeWorkspaceContract",
                "build_default_describe_rule_schema_drift",
                "build_default_describe_workspace_contract",
            ],
        )

    def test_application_directory_matches_allowed_anchor_shape(self) -> None:
        application_dir = Path(
            workspace_contract_application.__file__).resolve().parent
        entries = {
            path.name
            for path in application_dir.iterdir()
            if path.name != "__pycache__"
        }

        self.assertEqual(
            entries, {"__init__.py", "commands", "queries", "services"})

    def test_services_directory_matches_refactor_target_shape(self) -> None:
        services_dir = Path(
            workspace_contract_application.__file__).resolve().parent / "services"
        entries = {
            path.name
            for path in services_dir.iterdir()
            if path.name != "__pycache__"
        }

        self.assertEqual(
            entries,
            {
                "__init__.py",
                "rule_schema_validation",
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
        self.assertEqual(
            tuple(inspect.signature(DescribeRuleSchemaDrift).parameters),
            ("validation_service",),
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
                          "AGENT.md", created_files)
            self.assertEqual(result["updated_files"], ())

    def test_update_only_marks_changed_shared_docs_as_updated(self) -> None:
        with TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)

            build_default_bootstrap_project().execute(project_root)
            shared_doc_path = project_root / "agentic" / "rules" / "AGENT.md"
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

    def test_describe_reports_present_missing_and_local_extension_paths(self) -> None:
        with TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)

            build_default_bootstrap_project().execute(project_root)
            existing_shared_doc_path = project_root / "agentic" / "rules" / "AGENT.md"
            missing_shared_doc_path = project_root / \
                "agentic" / "rules" / "planning" / "PLANNING.md"
            missing_shared_doc_path.unlink()
            override_path = project_root / "agentic" / "rules" / "overrides" / "TESTS.md"
            project_specific_path = project_root / "agentic" / \
                "rules" / "project-specific" / "LOCAL.md"
            override_path.write_text("override\n", encoding="utf-8")
            project_specific_path.write_text("local\n", encoding="utf-8")

            summary = build_default_describe_workspace_contract().execute(project_root)

            self.assertTrue(summary.agentic_dir_exists)
            self.assertTrue(summary.config_exists)
            self.assertIn(existing_shared_doc_path, summary.shared_rule_paths)
            self.assertIn(missing_shared_doc_path,
                          summary.missing_shared_rule_paths)
            self.assertEqual(summary.override_paths, (override_path,))
            self.assertEqual(summary.project_specific_paths,
                             (project_specific_path,))


class RuleSchemaValidationApplicationTests(unittest.TestCase):
    def test_describe_rule_schema_drift_delegates_to_validation_service(self) -> None:
        class ValidationServiceStub:
            def __init__(self, result: RuleSchemaValidationResult) -> None:
                self.result = result
                self.calls: list[tuple[Path, bool]] = []

            def describe(
                self,
                project_root: Path,
                *,
                include_local_mirror: bool = True,
            ) -> RuleSchemaValidationResult:
                self.calls.append((project_root, include_local_mirror))
                return self.result

        project_root = Path("/tmp/example-project")
        expected_result = RuleSchemaValidationResult(
            packaged_documents=(Path("AGENT.md"),),
        )
        validation_service = ValidationServiceStub(expected_result)

        result = DescribeRuleSchemaDrift(
            validation_service=cast(Any, validation_service),
        ).execute(project_root, include_local_mirror=False)

        self.assertIs(result, expected_result)
        self.assertEqual(validation_service.calls, [(project_root, False)])

    def test_reports_no_drift_for_packaged_rules_and_bootstrapped_local_mirror(self) -> None:
        with TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)

            build_default_bootstrap_project().execute(project_root)

            result = build_default_describe_rule_schema_drift().execute(project_root)

            self.assertFalse(result.has_findings)
            self.assertIn(Path("AGENT.md"), result.packaged_documents)
            self.assertIn(Path("ddd") / "DDD.md", result.packaged_documents)
            self.assertIn(Path("feature") / "module" / "layers" /
                          "APPLICATION.md", result.local_documents)

    def test_reports_anchor_drift_in_local_mirror(self) -> None:
        with TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)

            build_default_bootstrap_project().execute(project_root)
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

            result = build_default_describe_rule_schema_drift().execute(project_root)

            self.assertTrue(result.has_findings)
            self.assertEqual(result.findings[0].scope, "local")
            self.assertEqual(result.findings[0].document_path, Path(
                "feature") / "module" / "layers" / "APPLICATION.md")
            self.assertEqual(result.findings[0].code, "anchor-profile-drift")
            self.assertIsNone(result.findings[0].section_heading)

    def test_reports_missing_managed_document_in_local_mirror(self) -> None:
        with TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)

            build_default_bootstrap_project().execute(project_root)
            missing_local_doc = project_root / "agentic" / \
                "rules" / "planning" / "PLANNING.md"
            missing_local_doc.unlink()

            result = build_default_describe_rule_schema_drift().execute(project_root)

            self.assertTrue(result.has_findings)
            self.assertEqual(result.findings[0].scope, "local")
            self.assertEqual(result.findings[0].document_path, Path(
                "planning") / "PLANNING.md")
            self.assertEqual(result.findings[0].code, "missing-local-document")
            self.assertIsNone(result.findings[0].section_heading)

    def test_can_exclude_local_mirror_validation(self) -> None:
        with TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)

            build_default_bootstrap_project().execute(project_root)
            local_agent_doc = project_root / "agentic" / "rules" / "AGENT.md"
            local_agent_doc.write_text("broken\n", encoding="utf-8")

            result = build_default_describe_rule_schema_drift().execute(
                project_root, include_local_mirror=False)

            self.assertFalse(result.has_findings)
            self.assertEqual(result.local_documents, ())


if __name__ == "__main__":
    unittest.main()
