import agentic.features.architecture_check.dependency_map as architecture_dependency_map
import agentic.features.architecture_check.dependency_map.application as architecture_dependency_map_application
import agentic.features.architecture_check.hotspots as architecture_hotspots
import agentic.features.architecture_check.hotspots.application as architecture_hotspots_application
import agentic.features.architecture_check.policy_check as architecture_policy_check
import agentic.features.architecture_check.policy_check.application as architecture_check_application
import agentic.features.architecture_check.policy_check.application.commands as architecture_check_application_commands
import agentic.features.architecture_check.policy_check.application.queries as architecture_check_application_queries
import agentic.features.architecture_check.policy_check.application.services as architecture_check_application_services
import inspect
from pathlib import Path
from typing import Any, cast
import unittest

from agentic.features.architecture_check.dependency_map.application import LoadConfigQuery
from agentic.features.architecture_check.dependency_map.infrastructure import ExtractorRuntime
from agentic.features.architecture_check.hotspots.application.queries import DescribeFileImportHotspotsQuery, FileImportHotspotEntry, FileImportHotspotsResult
from agentic.features.architecture_check.policy_check.application.commands.run_architecture_check import CheckResult, RunArchitectureCheckCommand
from agentic.features.architecture_check.policy_check.application.queries import ArchitectureSummary, BuildArchitectureReportQuery, DescribeArchitectureQuery, ViolationGroup


class ArchitectureCheckApplicationPackageTests(unittest.TestCase):
    def test_feature_seam_packages_export_staged_public_surfaces(self) -> None:
        self.assertEqual(
            architecture_dependency_map.__all__,
            [
                "BuildDependencyMapQuery",
                "BuildDependencyMapResult",
                "DependencyMapBuildError",
                "ExtractorRuntime",
                "ArchitectureCheckConfig",
                "ArchitectureCheckConfigError",
                "CheckerError",
                "ConfigLoadResult",
                "LoadConfigQuery",
                "build_default_build_dependency_map_query",
                "build_default_load_config_query",
                "build_dependency_map",
                "load_config",
            ],
        )
        self.assertEqual(
            architecture_policy_check.__all__,
            [
                "ArchitectureSummary",
                "BuildArchitectureReportQuery",
                "CheckResult",
                "CheckerError",
                "architecture_check_cli",
                "build_default_architecture_check_cli",
                "build_default_architecture_report_query",
                "describe_architecture",
                "run_architecture_check",
            ],
        )
        self.assertEqual(
            architecture_hotspots.__all__,
            [
                "DescribeFileImportHotspotsQuery",
                "FileImportHotspotEntry",
                "FileImportHotspotsResult",
                "build_default_describe_file_import_hotspots_query",
                "build_default_file_import_hotspots_view",
            ],
        )

    def test_module_roots_export_stable_builder_and_result_symbols(self) -> None:
        self.assertTrue(hasattr(architecture_dependency_map,
                        "BuildDependencyMapQuery"))
        self.assertTrue(hasattr(architecture_dependency_map,
                        "BuildDependencyMapResult"))
        self.assertTrue(hasattr(architecture_dependency_map,
                        "DependencyMapBuildError"))
        self.assertTrue(
            hasattr(architecture_dependency_map, "LoadConfigQuery"))
        self.assertTrue(
            hasattr(architecture_dependency_map, "ExtractorRuntime"))
        self.assertIs(
            architecture_dependency_map.ExtractorRuntime, ExtractorRuntime)
        self.assertTrue(hasattr(architecture_policy_check,
                        "build_default_architecture_report_query"))
        self.assertTrue(hasattr(architecture_policy_check,
                        "build_default_architecture_check_cli"))
        self.assertTrue(hasattr(architecture_hotspots,
                        "build_default_file_import_hotspots_view"))

    def test_dependency_map_application_exports_build_and_load_queries(self) -> None:
        self.assertEqual(
            architecture_dependency_map_application.__all__,
            [
                "BuildDependencyMapQuery",
                "BuildDependencyMapResult",
                "DependencyMapBuildError",
                "LoadConfigQuery",
                "build_default_build_dependency_map_query",
                "build_dependency_map",
                "load_config",
            ],
        )

    def test_application_package_exports_only_policy_check_public_seam(self) -> None:
        self.assertEqual(
            architecture_check_application.__all__,
            [
                "ArchitectureSummary",
                "BuildArchitectureReportQuery",
                "CheckResult",
                "CheckerError",
                "describe_architecture",
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

    def test_application_keeps_shim_only_query_symbols_out_of_public_exports(self) -> None:
        self.assertNotIn(
            "DescribeFileImportHotspotsQuery",
            architecture_check_application.__all__,
        )
        self.assertNotIn(
            "FileImportHotspotEntry",
            architecture_check_application.__all__,
        )
        self.assertNotIn(
            "FileImportHotspotsResult",
            architecture_check_application.__all__,
        )
        self.assertNotIn(
            "ViolationGroup",
            architecture_check_application.__all__,
        )
        self.assertNotIn(
            "build_default_architecture_report_query",
            architecture_check_application.__all__,
        )
        self.assertNotIn(
            "build_default_describe_file_import_hotspots_query",
            architecture_check_application.__all__,
        )

        self.assertFalse(hasattr(architecture_check_application,
                         "DescribeFileImportHotspotsQuery"))
        self.assertFalse(
            hasattr(architecture_check_application, "FileImportHotspotEntry"))
        self.assertFalse(
            hasattr(architecture_check_application, "FileImportHotspotsResult"))
        self.assertFalse(
            hasattr(architecture_check_application, "ViolationGroup"))
        self.assertFalse(hasattr(architecture_check_application,
                         "build_default_architecture_report_query"))
        self.assertFalse(hasattr(architecture_check_application,
                         "build_default_describe_file_import_hotspots_query"))

    def test_commands_package_exports_only_public_seam(self) -> None:
        self.assertEqual(
            architecture_check_application_commands.__all__,
            ["CheckResult", "RunArchitectureCheckCommand", "run_architecture_check"],
        )

    def test_queries_package_exports_only_policy_check_seam(self) -> None:
        self.assertEqual(
            architecture_check_application_queries.__all__,
            [
                "ArchitectureSummary",
                "BuildArchitectureReportQuery",
                "DescribeArchitectureQuery",
                "ViolationGroup",
                "build_default_architecture_report_query",
                "describe_architecture",
            ],
        )

    def test_hotspots_application_exports_only_hotspot_query_surface(self) -> None:
        self.assertEqual(
            architecture_hotspots_application.__all__,
            [
                "DescribeFileImportHotspotsQuery",
                "FileImportHotspotEntry",
                "FileImportHotspotsResult",
                "build_default_describe_file_import_hotspots_query",
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

    def test_feature_root_contains_staged_sibling_module_seams(self) -> None:
        feature_dir = Path(
            architecture_dependency_map.__file__).resolve().parent.parent
        entries = {
            path.name
            for path in feature_dir.iterdir()
            if path.name != "__pycache__"
        }

        self.assertIn("dependency_map", entries)
        self.assertIn("policy_check", entries)
        self.assertIn("hotspots", entries)
        self.assertNotIn("checker", entries)

    def test_dependency_map_package_contains_owner_layers(self) -> None:
        dependency_map_dir = Path(
            architecture_dependency_map.__file__).resolve().parent
        entries = {
            path.name
            for path in dependency_map_dir.iterdir()
            if path.name != "__pycache__"
        }

        self.assertEqual(
            entries,
            {"__init__.py", "application", "domain", "infrastructure"},
        )

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
            tuple(inspect.signature(DescribeFileImportHotspotsQuery).parameters),
            ("file_import_hotspots_service",),
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
                DescribeFileImportHotspotsQuery
            ).parameters["file_import_hotspots_service"].default,
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
            {"__init__.py", "architecture_check_service.py",
                "architecture_report_builder", "architecture_summary_service.py"},
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
                "service.py",
                "violation_renderer.py",
            },
        )

    def test_service_constructors_require_non_nullable_collaborators(self) -> None:
        from agentic.features.architecture_check.dependency_map.application.services.config_load_service import ConfigLoadService
        from agentic.features.architecture_check.hotspots.application.services.file_import_hotspots_service import FileImportHotspotsService
        from agentic.features.architecture_check.policy_check.application.services.architecture_check_service import ArchitectureCheckService
        from agentic.features.architecture_check.policy_check.application.services.architecture_summary_service import ArchitectureSummaryService
        from agentic.features.architecture_check.policy_check.application.services.architecture_report_builder import ArchitectureReportBuilder
        from agentic.features.architecture_check.policy_check.application.services.architecture_report_builder.architecture_evaluator import ArchitectureEvaluator

        self.assertEqual(
            tuple(inspect.signature(ArchitectureCheckService).parameters),
            ("summary_service",),
        )
        self.assertEqual(
            tuple(inspect.signature(FileImportHotspotsService).parameters),
            (
                "config_load_service",
                "extractor_runtime_factory",
                "extractor_spec_registry",
                "dependency_graph_builder",
            ),
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
                "build_dependency_map_query",
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
            FileImportHotspotsService,
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
        runtime = cast(Any, object())

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
        runtime = cast(Any, object())

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
        runtime = cast(Any, object())
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

    def test_file_import_hotspots_query_delegates_to_service(self) -> None:
        class FileImportHotspotsServiceStub:
            def __init__(self, result: FileImportHotspotsResult) -> None:
                self.result = result
                self.calls: list[tuple[Path, str | None,
                                       str, bool, object | None]] = []

            def describe(
                self,
                project_root: Path,
                explicit_config_path: str | None = None,
                *,
                sort_by: str = "imported_by_count",
                descending: bool = True,
                extractor_runtime: object | None = None,
            ) -> FileImportHotspotsResult:
                self.calls.append(
                    (project_root, explicit_config_path,
                     sort_by, descending, extractor_runtime)
                )
                return self.result

        project_root = Path("/tmp/example-project")
        result = FileImportHotspotsResult(
            entries=(
                FileImportHotspotEntry(
                    path="src/example.py",
                    imports_count=1,
                    imported_by_count=3,
                ),
            ),
            sort_by="imported_by_count",
            descending=True,
        )
        service = FileImportHotspotsServiceStub(result)
        runtime = cast(Any, object())

        query = DescribeFileImportHotspotsQuery(
            file_import_hotspots_service=cast(Any, service)
        )

        described = query.describe(
            project_root,
            "custom.yaml",
            sort_by="imports_count",
            descending=False,
            extractor_runtime=runtime,
        )

        self.assertIs(described, result)
        self.assertEqual(
            service.calls,
            [(project_root, "custom.yaml", "imports_count", False, runtime)],
        )

    def test_file_import_hotspots_result_serializes_entries(self) -> None:
        result = FileImportHotspotsResult(
            entries=(
                FileImportHotspotEntry(
                    path="src/a.py",
                    imports_count=2,
                    imported_by_count=5,
                ),
            ),
            sort_by="imported_by_count",
            descending=True,
        )

        self.assertEqual(
            result.to_json_dict(),
            {
                "entries": [
                    {
                        "path": "src/a.py",
                        "imports_count": 2,
                        "imported_by_count": 5,
                    }
                ],
                "sort_by": "imported_by_count",
                "descending": True,
            },
        )


class FileImportHotspotsServiceTests(unittest.TestCase):
    def test_service_counts_tracked_file_relationships_and_sorts_by_importers_desc_by_default(self) -> None:
        from agentic.features.architecture_check.dependency_map.application.services.dependency_map_builder import DependencyGraphBuilder
        from agentic.features.architecture_check.dependency_map.domain import ArchitectureCheckConfig, ConfigLoadResult, DependencyGraph, ExtractedFile, ExtractionResult, ExtractionSummary
        from agentic.features.architecture_check.hotspots.application.services.file_import_hotspots_service import FileImportHotspotsService

        class ConfigLoadServiceStub:
            def __init__(self, result: ConfigLoadResult) -> None:
                self.result = result
                self.calls: list[tuple[Path, str | None]] = []

            def load(self, project_root: Path, explicit_config_path: str | None = None) -> ConfigLoadResult:
                self.calls.append((project_root, explicit_config_path))
                return self.result

        class RuntimeStub:
            def __init__(self, extraction_result: ExtractionResult) -> None:
                self.extraction_result = extraction_result
                self.calls: list[tuple[object, Path, list[str]]] = []

            def run(self, spec: object, project_root: Path, exclusions: list[str]) -> ExtractionResult:
                self.calls.append((spec, project_root, exclusions))
                return self.extraction_result

        class RuntimeFactoryStub:
            def __init__(self, runtime: RuntimeStub) -> None:
                self.runtime = runtime
                self.create_calls = 0

            def create(self) -> RuntimeStub:
                self.create_calls += 1
                return self.runtime

        class ExtractorSpecRegistryStub:
            def __init__(self, spec: object) -> None:
                self.spec = spec
                self.calls: list[str] = []

            def get(self, language: str) -> object:
                self.calls.append(language)
                return self.spec

        project_root = Path("/tmp/example-project")
        config = ArchitectureCheckConfig(
            language="python", exclusions=["tests/**"])
        load_result = ConfigLoadResult(
            path=project_root / "agentic" / "agentic.yaml",
            config=config,
            source_format="yaml",
        )
        extraction_result = ExtractionResult(
            files={
                "src/a.py": ExtractedFile(imports=["src/b.py", "src/b.py", "src/c.py", "requests"], classes=[], functions=[]),
                "src/b.py": ExtractedFile(imports=[], classes=[], functions=[]),
                "src/c.py": ExtractedFile(imports=[], classes=[], functions=[]),
                "src/d.py": ExtractedFile(imports=["src/b.py"], classes=[], functions=[]),
            },
            summary=ExtractionSummary(
                files_found=4, files_excluded=0, files_checked=4),
        )
        runtime = RuntimeStub(extraction_result)
        runtime_factory = RuntimeFactoryStub(runtime)
        spec = object()
        registry = ExtractorSpecRegistryStub(spec)
        graph_builder = DependencyGraphBuilder()
        service = FileImportHotspotsService(
            config_load_service=cast(Any, ConfigLoadServiceStub(load_result)),
            extractor_runtime_factory=cast(Any, runtime_factory),
            extractor_spec_registry=cast(Any, registry),
            dependency_graph_builder=graph_builder,
        )

        result = service.describe(project_root, "custom.yaml")

        self.assertEqual(runtime_factory.create_calls, 1)
        self.assertEqual(registry.calls, ["python"])
        self.assertEqual(runtime.calls, [(spec, project_root, ["tests/**"])])
        self.assertEqual(
            result.entries,
            (
                FileImportHotspotEntry(
                    path="src/b.py", imports_count=0, imported_by_count=2),
                FileImportHotspotEntry(
                    path="src/c.py", imports_count=0, imported_by_count=1),
                FileImportHotspotEntry(
                    path="src/a.py", imports_count=2, imported_by_count=0),
                FileImportHotspotEntry(
                    path="src/d.py", imports_count=1, imported_by_count=0),
            ),
        )

        graph = DependencyGraph()
        graph.add_edge("src/a.py", "src/b.py")
        graph.add_edge("src/a.py", "src/b.py")
        graph.add_edge("src/a.py", "src/c.py")
        graph.add_edge("src/a.py", "requests")
        graph.add_edge("src/d.py", "src/b.py")

        built_graph = graph_builder.build(extraction_result.files)
        self.assertEqual(tuple(built_graph.edges), tuple(graph.edges))

    def test_service_supports_import_count_sort_and_uses_explicit_runtime(self) -> None:
        from agentic.features.architecture_check.dependency_map.domain import ArchitectureCheckConfig, ConfigLoadResult, DependencyGraph, ExtractedFile, ExtractionResult, ExtractionSummary
        from agentic.features.architecture_check.hotspots.application.services.file_import_hotspots_service import FileImportHotspotsService

        class ConfigLoadServiceStub:
            def __init__(self, result: ConfigLoadResult) -> None:
                self.result = result

            def load(self, project_root: Path, explicit_config_path: str | None = None) -> ConfigLoadResult:
                return self.result

        class RuntimeStub:
            def __init__(self, extraction_result: ExtractionResult) -> None:
                self.extraction_result = extraction_result
                self.calls: list[tuple[object, Path, list[str]]] = []

            def run(self, spec: object, project_root: Path, exclusions: list[str]) -> ExtractionResult:
                self.calls.append((spec, project_root, exclusions))
                return self.extraction_result

        class RuntimeFactoryStub:
            def __init__(self) -> None:
                self.create_calls = 0

            def create(self) -> object:
                self.create_calls += 1
                return object()

        class ExtractorSpecRegistryStub:
            def __init__(self, spec: object) -> None:
                self.spec = spec

            def get(self, language: str) -> object:
                return self.spec

        class DependencyGraphBuilderStub:
            def __init__(self, graph: DependencyGraph) -> None:
                self.graph = graph

            def build(self, architecture_map: dict[str, object]) -> DependencyGraph:
                return self.graph

        project_root = Path("/tmp/example-project")
        load_result = ConfigLoadResult(
            path=project_root / "agentic" / "agentic.yaml",
            config=ArchitectureCheckConfig(language="python", exclusions=[]),
            source_format="yaml",
        )
        extraction_result = ExtractionResult(
            files={
                "src/a.py": ExtractedFile(imports=[], classes=[], functions=[]),
                "src/b.py": ExtractedFile(imports=[], classes=[], functions=[]),
                "src/c.py": ExtractedFile(imports=[], classes=[], functions=[]),
            },
            summary=ExtractionSummary(
                files_found=3, files_excluded=0, files_checked=3),
        )
        graph = DependencyGraph()
        graph.add_edge("src/a.py", "src/b.py")
        graph.add_edge("src/a.py", "src/c.py")
        graph.add_edge("src/b.py", "src/c.py")
        graph.add_edge("src/a.py", "urllib")
        runtime = RuntimeStub(extraction_result)
        runtime_factory = RuntimeFactoryStub()
        spec = object()
        service = FileImportHotspotsService(
            config_load_service=cast(Any, ConfigLoadServiceStub(load_result)),
            extractor_runtime_factory=cast(Any, runtime_factory),
            extractor_spec_registry=cast(Any, ExtractorSpecRegistryStub(spec)),
            dependency_graph_builder=cast(
                Any, DependencyGraphBuilderStub(graph)),
        )

        result = service.describe(
            project_root,
            sort_by="imports_count",
            extractor_runtime=cast(Any, runtime),
        )

        self.assertEqual(runtime_factory.create_calls, 0)
        self.assertEqual(runtime.calls, [(spec, project_root, [])])
        self.assertEqual(
            result.entries,
            (
                FileImportHotspotEntry(
                    path="src/a.py", imports_count=2, imported_by_count=0),
                FileImportHotspotEntry(
                    path="src/b.py", imports_count=1, imported_by_count=1),
                FileImportHotspotEntry(
                    path="src/c.py", imports_count=0, imported_by_count=2),
            ),
        )
        self.assertEqual(result.sort_by, "imports_count")
        self.assertTrue(result.descending)


if __name__ == "__main__":
    unittest.main()
