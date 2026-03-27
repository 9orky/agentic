import agentic.features.architecture_check.checker.application as architecture_check_application
import agentic.features.architecture_check.checker.application.commands as architecture_check_application_commands
import agentic.features.architecture_check.checker.application.queries as architecture_check_application_queries
import agentic.features.architecture_check.checker.application.services as architecture_check_application_services
import inspect
from pathlib import Path
from typing import Any, cast
import unittest

from agentic.features.architecture_check.checker.application.commands.run_architecture_check import CheckResult, RunArchitectureCheckCommand
from agentic.features.architecture_check.checker.application.queries import ArchitectureSummary, BuildArchitectureReportQuery, DescribeArchitectureQuery, LoadConfigQuery, ViolationGroup


class ArchitectureCheckApplicationPackageTests(unittest.TestCase):
    def test_application_package_exports_only_public_seam_and_next_ui_query(self) -> None:
        self.assertEqual(
            architecture_check_application.__all__,
            [
                "ArchitectureSummary",
                "BuildArchitectureReportQuery",
                "CheckResult",
                "CheckerError",
                "describe_architecture",
                "load_config",
                "run_architecture_check",
            ],
        )

    def test_application_does_not_leak_service_helper_attributes(self) -> None:
        self.assertFalse(
            hasattr(architecture_check_application, "build_architecture_report"))
        self.assertFalse(
            hasattr(architecture_check_application, "build_dot_report"))
        self.assertFalse(
            hasattr(architecture_check_application, "build_violation_groups"))

    def test_commands_package_exports_only_public_seam(self) -> None:
        self.assertEqual(
            architecture_check_application_commands.__all__,
            ["CheckResult", "RunArchitectureCheckCommand", "run_architecture_check"],
        )

    def test_queries_package_exports_only_public_seam_and_report_query(self) -> None:
        self.assertEqual(
            architecture_check_application_queries.__all__,
            [
                "ArchitectureSummary",
                "BuildArchitectureReportQuery",
                "DescribeArchitectureQuery",
                "LoadConfigQuery",
                "ViolationGroup",
                "build_default_architecture_report_query",
                "describe_architecture",
                "load_config",
            ],
        )

    def test_application_directory_matches_allowed_anchor_shape(self) -> None:
        application_dir = Path(
            architecture_check_application.__file__).resolve().parent
        entries = {
            path.name
            for path in application_dir.iterdir()
            if path.name != "__pycache__"
        }

        self.assertEqual(
            entries, {"__init__.py", "commands", "queries", "services"})

    def test_queries_and_commands_depend_on_service_or_adapter_boundaries(self) -> None:
        self.assertEqual(
            tuple(inspect.signature(RunArchitectureCheckCommand).parameters),
            ("check_service",),
        )
        self.assertEqual(
            tuple(inspect.signature(DescribeArchitectureQuery).parameters),
            ("summary_service",),
        )
        self.assertEqual(
            tuple(inspect.signature(LoadConfigQuery).parameters),
            ("config_load_service",),
        )
        self.assertEqual(
            tuple(inspect.signature(BuildArchitectureReportQuery).parameters),
            ("report_builder",),
        )

        self.assertIs(
            inspect.signature(
                RunArchitectureCheckCommand).parameters["check_service"].default,
            inspect._empty,
        )
        self.assertIs(
            inspect.signature(
                DescribeArchitectureQuery).parameters["summary_service"].default,
            inspect._empty,
        )
        self.assertIs(
            inspect.signature(
                LoadConfigQuery).parameters["config_load_service"].default,
            inspect._empty,
        )
        self.assertIs(
            inspect.signature(
                BuildArchitectureReportQuery).parameters["report_builder"].default,
            inspect._empty,
        )

    def test_services_directory_matches_refactor_target_shape(self) -> None:
        services_dir = Path(
            architecture_check_application.__file__).resolve().parent / "services"
        entries = {
            path.name
            for path in services_dir.iterdir()
            if path.name != "__pycache__"
        }

        self.assertEqual(
            entries,
            {
                "__init__.py",
                "architecture_check_service.py",
                "architecture_report_builder",
                "architecture_summary_service.py",
                "config_load_service.py",
            },
        )

    def test_services_anchor_exports_no_cross_layer_surface(self) -> None:
        self.assertEqual(architecture_check_application_services.__all__, [])

    def test_report_builder_service_uses_folder_form_with_minimal_public_api(self) -> None:
        report_builder_dir = (
            Path(architecture_check_application.__file__).resolve().parent
            / "services"
            / "architecture_report_builder"
        )
        entries = {
            path.name
            for path in report_builder_dir.iterdir()
            if path.name != "__pycache__"
        }

        self.assertEqual(
            entries,
            {
                "__init__.py",
                "architecture_check_report.py",
                "architecture_evaluator.py",
                "dependency_graph_builder.py",
                "service.py",
                "violation_renderer.py",
            },
        )

    def test_service_constructors_require_non_nullable_collaborators(self) -> None:
        from agentic.features.architecture_check.checker.application.services.architecture_check_service import ArchitectureCheckService
        from agentic.features.architecture_check.checker.application.services.architecture_summary_service import ArchitectureSummaryService
        from agentic.features.architecture_check.checker.application.services.config_load_service import ConfigLoadService
        from agentic.features.architecture_check.checker.application.services.architecture_report_builder import ArchitectureReportBuilder
        from agentic.features.architecture_check.checker.application.services.architecture_report_builder.architecture_evaluator import ArchitectureEvaluator

        self.assertEqual(
            tuple(inspect.signature(ArchitectureCheckService).parameters),
            ("summary_service", "extractor_runtime_factory"),
        )
        self.assertEqual(
            tuple(inspect.signature(ArchitectureSummaryService).parameters),
            ("report_builder", "violation_renderer"),
        )
        self.assertEqual(
            tuple(inspect.signature(ConfigLoadService).parameters),
            ("config_loader",),
        )
        self.assertEqual(
            tuple(inspect.signature(ArchitectureReportBuilder).parameters),
            (
                "config_load_service",
                "extractor_runtime_factory",
                "extractor_spec_registry",
                "dependency_graph_builder",
                "architecture_evaluator",
                "violation_dot_renderer",
            ),
        )
        self.assertEqual(
            tuple(inspect.signature(ArchitectureEvaluator).parameters),
            ("policy_evaluator",),
        )

        for cls in (
            ArchitectureCheckService,
            ArchitectureSummaryService,
            ConfigLoadService,
            ArchitectureReportBuilder,
            ArchitectureEvaluator,
        ):
            for parameter in inspect.signature(cls).parameters.values():
                self.assertIs(parameter.default, inspect._empty)


class ArchitectureCheckApplicationDelegationTests(unittest.TestCase):
    def test_run_command_delegates_to_check_service(self) -> None:
        class CheckServiceStub:
            def __init__(self, summary: ArchitectureSummary) -> None:
                self.summary = summary
                self.calls: list[tuple[Path, str | None, object | None]] = []

            def check(
                self,
                project_root: Path,
                explicit_config_path: str | None = None,
                *,
                extractor_runtime: object | None = None,
            ) -> ArchitectureSummary:
                self.calls.append(
                    (project_root, explicit_config_path, extractor_runtime))
                return self.summary

        project_root = Path("/tmp/example-project")
        summary = ArchitectureSummary(
            project_root=project_root,
            config_path=project_root / "agentic" / "agentic.yaml",
            config_format="yaml",
            language="python",
            runtime_command="python",
            files_found=3,
            files_excluded=1,
            files_checked=2,
            violations=("violation",),
        )
        check_service = CheckServiceStub(summary)
        runtime = object()

        result = RunArchitectureCheckCommand(
            check_service=cast(Any, check_service)
        ).run(project_root, "custom.yaml", extractor_runtime=runtime)

        self.assertEqual(
            check_service.calls,
            [(project_root, "custom.yaml", runtime)],
        )
        self.assertEqual(
            result,
            CheckResult(
                project_root=project_root,
                config_path=project_root / "agentic" / "agentic.yaml",
                config_format="yaml",
                files_found=3,
                files_excluded=1,
                files_checked=2,
                violations=["violation"],
            ),
        )

    def test_describe_query_delegates_to_summary_service(self) -> None:
        class SummaryServiceStub:
            def __init__(self, summary: ArchitectureSummary) -> None:
                self.summary = summary
                self.calls: list[tuple[Path, str | None, object | None]] = []

            def describe(
                self,
                project_root: Path,
                explicit_config_path: str | None = None,
                *,
                extractor_runtime: object | None = None,
            ) -> ArchitectureSummary:
                self.calls.append(
                    (project_root, explicit_config_path, extractor_runtime))
                return self.summary

        project_root = Path("/tmp/example-project")
        summary = ArchitectureSummary(
            project_root=project_root,
            config_path=project_root / "agentic" / "agentic.yaml",
            config_format="yaml",
            language="python",
            runtime_command="python",
        )
        summary_service = SummaryServiceStub(summary)
        runtime = object()

        result = DescribeArchitectureQuery(
            summary_service=cast(Any, summary_service)
        ).describe(project_root, "custom.yaml", extractor_runtime=runtime)

        self.assertIs(result, summary)
        self.assertEqual(
            summary_service.calls,
            [(project_root, "custom.yaml", runtime)],
        )

    def test_report_query_delegates_to_report_builder(self) -> None:
        class ReportBuilderStub:
            def __init__(self) -> None:
                self.build_calls: list[tuple[Path,
                                             str | None, object | None]] = []

            def build_artifacts(
                self,
                project_root: Path,
                explicit_config_path: str | None = None,
                *,
                extractor_runtime: object | None = None,
            ) -> object:
                self.build_calls.append(
                    (project_root, explicit_config_path, extractor_runtime))

                class ReportStub:
                    check_error = None
                    violations = ("violation",)
                    files_found = 5
                    files_excluded = 1
                    files_checked = 4

                    def to_json_dict(self) -> dict[str, object]:
                        return {"ok": True}

                class ArtifactsStub:
                    report = ReportStub()
                    dot_report = "digraph {}"
                    violation_groups = (("Group", ("entry",)),)

                return ArtifactsStub()

        project_root = Path("/tmp/example-project")
        report_builder = ReportBuilderStub()
        runtime = object()
        query = BuildArchitectureReportQuery(
            report_builder=cast(Any, report_builder))

        report = query.execute(project_root, "custom.yaml",
                               extractor_runtime=runtime)

        self.assertEqual(report.dot_report, "digraph {}")
        self.assertEqual(report.violation_groups, (ViolationGroup(
            title="Group", entries=("entry",)),))
        self.assertEqual(report.violations, ("violation",))
        self.assertEqual(report.files_found, 5)
        self.assertEqual(report.to_json_dict(), {"ok": True})
        self.assertEqual(
            report_builder.build_calls,
            [(project_root, "custom.yaml", runtime)],
        )


if __name__ == "__main__":
    unittest.main()
