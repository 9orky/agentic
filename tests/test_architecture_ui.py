import agentic.features.architecture_check as architecture_check_boundary
import agentic.features.architecture_check.checker.ui as architecture_check_ui
import agentic.features.architecture_check.checker.ui.services as architecture_check_ui_services
import agentic.features.architecture_check.checker.ui.views as architecture_check_ui_views
import agentic.features.architecture_check.cli as architecture_check_feature_cli
import click
import inspect
from pathlib import Path
import unittest

from agentic.features.architecture_check.checker.ui import ArchitectureCheckCli


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
            ["GroupedViolationView", "JsonReportView"],
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
                "grouped_violation_view",
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

    def test_ui_registration_export_registers_check_command(self) -> None:
        app = click.Group()

        architecture_check_ui.architecture_check_cli(app)

        self.assertIn("check", app.commands)


if __name__ == "__main__":
    unittest.main()
