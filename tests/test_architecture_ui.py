import agentic.features.architecture_check as architecture_check_boundary
import agentic.features.architecture_check.checker.ui as architecture_check_ui
import agentic.features.architecture_check.checker.ui.services as architecture_check_ui_services
import agentic.features.architecture_check.checker.ui.views as architecture_check_ui_views
import agentic.features.architecture_check.cli as architecture_check_feature_cli
import click
import inspect
from pathlib import Path
from typing import Any, cast
import unittest
from unittest import mock

from agentic.features.architecture_check.checker.ui import ArchitectureCheckCli
from agentic.features.architecture_check.checker.application import FileImportHotspotEntry, FileImportHotspotsResult


class ArchitectureCheckBoundaryAndUiTests(unittest.TestCase):
    def test_feature_boundary_exports_expected_public_seam(self) -> None:
        self.assertEqual(
            architecture_check_boundary.__all__,
            [
                "ArchitectureSummary",
                "ArchitectureCheckConfig",
                "ArchitectureCheckConfigError",
                "CheckResult",
                "CheckerError",
                "ConfigLoadResult",
                "describe_architecture",
                "load_config",
                "run_architecture_check",
            ],
        )

    def test_feature_boundary_does_not_export_hotspots_query_surface(self) -> None:
        self.assertNotIn(
            "DescribeFileImportHotspotsQuery",
            architecture_check_boundary.__all__,
        )
        self.assertNotIn(
            "FileImportHotspotEntry",
            architecture_check_boundary.__all__,
        )
        self.assertNotIn(
            "FileImportHotspotsResult",
            architecture_check_boundary.__all__,
        )
        self.assertFalse(
            hasattr(architecture_check_boundary,
                    "DescribeFileImportHotspotsQuery")
        )
        self.assertFalse(
            hasattr(architecture_check_boundary, "FileImportHotspotEntry")
        )
        self.assertFalse(
            hasattr(architecture_check_boundary, "FileImportHotspotsResult")
        )

    def test_feature_cli_wrapper_exports_only_registration_seam(self) -> None:
        self.assertEqual(
            architecture_check_feature_cli.__all__,
            ["architecture_check_cli"],
        )

    def test_ui_package_exports_expected_public_seam(self) -> None:
        self.assertEqual(
            architecture_check_ui.__all__,
            ["ArchitectureCheckCli", "architecture_check_cli"],
        )

    def test_ui_service_and_view_packages_export_expected_public_seams(self) -> None:
        self.assertEqual(
            architecture_check_ui_services.__all__,
            ["CheckSummaryPresenter"],
        )
        self.assertEqual(
            architecture_check_ui_views.__all__,
            ["FileImportHotspotsView", "GroupedViolationView", "JsonReportView"],
        )

    def test_ui_directory_matches_allowed_anchor_shape(self) -> None:
        ui_dir = Path(architecture_check_ui.__file__).resolve().parent
        entries = {
            path.name
            for path in ui_dir.iterdir()
            if path.name != "__pycache__"
        }

        self.assertEqual(
            entries, {"__init__.py", "cli.py", "services", "views"})

    def test_ui_cli_constructor_requires_non_nullable_collaborators(self) -> None:
        self.assertEqual(
            tuple(inspect.signature(ArchitectureCheckCli).parameters),
            (
                "build_architecture_report_query",
                "describe_file_import_hotspots_query",
                "grouped_violation_view",
                "file_import_hotspots_view",
                "json_report_view",
                "check_summary_presenter",
            ),
        )

        for parameter in inspect.signature(ArchitectureCheckCli).parameters.values():
            self.assertIs(parameter.default, inspect._empty)

    def test_feature_cli_wrapper_registers_check_command(self) -> None:
        app = click.Group()

        architecture_check_feature_cli.architecture_check_cli(app)

        self.assertIn("check", app.commands)
        self.assertIn("hotspots", app.commands)

    def test_ui_registration_export_registers_check_command(self) -> None:
        app = click.Group()

        architecture_check_ui.architecture_check_cli(app)

        self.assertIn("check", app.commands)
        self.assertIn("hotspots", app.commands)

    def test_run_hotspots_renders_text_output(self) -> None:
        class ReportQueryStub:
            def execute(self, project_root: Path, explicit_config_path: str | None = None, *, extractor_runtime: object | None = None) -> object:
                raise AssertionError("check query should not be used")

        class HotspotsQueryStub:
            def __init__(self, result: FileImportHotspotsResult) -> None:
                self.result = result
                self.calls: list[tuple[Path, str | None, str, bool]] = []

            def describe(self, project_root: Path, explicit_config_path: str | None = None, *, sort_by: str = "imported_by_count", descending: bool = True, extractor_runtime: object | None = None) -> FileImportHotspotsResult:
                self.calls.append(
                    (project_root, explicit_config_path, sort_by, descending))
                return self.result

        class GroupedViolationViewStub:
            def render(self, groups: tuple[object, ...]) -> str:
                return ""

        class FileImportHotspotsViewStub:
            def __init__(self) -> None:
                self.rendered: FileImportHotspotsResult | None = None

            def render(self, result: FileImportHotspotsResult) -> str:
                self.rendered = result
                return "hotspots output"

        class JsonReportViewStub:
            def render(self, payload: dict[str, Any]) -> str:
                return "json output"

        class CheckSummaryPresenterStub:
            def render(self, files_found: int, files_excluded: int, files_checked: int) -> str:
                return "summary"

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
        hotspots_query = HotspotsQueryStub(result)
        hotspots_view = FileImportHotspotsViewStub()
        cli = ArchitectureCheckCli(
            build_architecture_report_query=cast(Any, ReportQueryStub()),
            describe_file_import_hotspots_query=cast(Any, hotspots_query),
            grouped_violation_view=cast(Any, GroupedViolationViewStub()),
            file_import_hotspots_view=cast(Any, hotspots_view),
            json_report_view=cast(Any, JsonReportViewStub()),
            check_summary_presenter=cast(Any, CheckSummaryPresenterStub()),
        )

        with mock.patch("click.echo") as echo_mock:
            exit_code = cli.run_hotspots(
                ".", None, "imported_by_count", True, "text")

        self.assertEqual(exit_code, 0)
        self.assertEqual(len(hotspots_query.calls), 1)
        self.assertIs(hotspots_view.rendered, result)
        echo_mock.assert_called_once_with("hotspots output")

    def test_run_hotspots_renders_json_output(self) -> None:
        class ReportQueryStub:
            def execute(self, project_root: Path, explicit_config_path: str | None = None, *, extractor_runtime: object | None = None) -> object:
                raise AssertionError("check query should not be used")

        class HotspotsQueryStub:
            def __init__(self, result: FileImportHotspotsResult) -> None:
                self.result = result

            def describe(self, project_root: Path, explicit_config_path: str | None = None, *, sort_by: str = "imported_by_count", descending: bool = True, extractor_runtime: object | None = None) -> FileImportHotspotsResult:
                return self.result

        class GroupedViolationViewStub:
            def render(self, groups: tuple[object, ...]) -> str:
                return ""

        class FileImportHotspotsViewStub:
            def render(self, result: FileImportHotspotsResult) -> str:
                return "text output"

        class JsonReportViewStub:
            def __init__(self) -> None:
                self.payload: dict[str, Any] | None = None

            def render(self, payload: dict[str, Any]) -> str:
                self.payload = payload
                return "json output"

        class CheckSummaryPresenterStub:
            def render(self, files_found: int, files_excluded: int, files_checked: int) -> str:
                return "summary"

        result = FileImportHotspotsResult(
            entries=(),
            sort_by="imports_count",
            descending=False,
        )
        json_view = JsonReportViewStub()
        cli = ArchitectureCheckCli(
            build_architecture_report_query=cast(Any, ReportQueryStub()),
            describe_file_import_hotspots_query=cast(
                Any, HotspotsQueryStub(result)),
            grouped_violation_view=cast(Any, GroupedViolationViewStub()),
            file_import_hotspots_view=cast(Any, FileImportHotspotsViewStub()),
            json_report_view=cast(Any, json_view),
            check_summary_presenter=cast(Any, CheckSummaryPresenterStub()),
        )

        with mock.patch("click.echo") as echo_mock:
            exit_code = cli.run_hotspots(
                ".", None, "imports_count", False, "json")

        self.assertEqual(exit_code, 0)
        self.assertEqual(
            json_view.payload,
            {
                "entries": [],
                "sort_by": "imports_count",
                "descending": False,
            },
        )
        echo_mock.assert_called_once_with("json output")


if __name__ == "__main__":
    unittest.main()
