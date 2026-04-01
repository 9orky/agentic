from __future__ import annotations

from pathlib import Path
from typing import Literal, Protocol, cast

import click

from ..application.queries.build_architecture_report import BuildArchitectureReportResult
from .services import CheckSummaryPresenter
from .views import GroupedViolationView, JsonReportView
from ...hotspots.application.services.file_import_hotspots_service import FileImportHotspotsResult


FileImportHotspotsSortBy = Literal["imported_by_count", "imports_count"]


class BuildArchitectureReportQueryLike(Protocol):
    def execute(
        self,
        project_root: Path,
        explicit_config_path: str | None = None,
        *,
        extractor_runtime: object | None = None,
    ) -> BuildArchitectureReportResult:
        ...


class DescribeFileImportHotspotsQueryLike(Protocol):
    def describe(
        self,
        project_root: Path,
        explicit_config_path: str | None = None,
        *,
        sort_by: FileImportHotspotsSortBy = "imported_by_count",
        descending: bool = True,
        extractor_runtime: object | None = None,
    ) -> FileImportHotspotsResult:
        ...


class FileImportHotspotsViewLike(Protocol):
    def render(self, result: object) -> str:
        ...


class ArchitectureCheckCli:
    def __init__(
        self,
        *,
        build_architecture_report_query: BuildArchitectureReportQueryLike,
        describe_file_import_hotspots_query: DescribeFileImportHotspotsQueryLike,
        grouped_violation_view: GroupedViolationView,
        file_import_hotspots_view: FileImportHotspotsViewLike,
        json_report_view: JsonReportView,
        check_summary_presenter: CheckSummaryPresenter,
    ) -> None:
        self._build_architecture_report_query = build_architecture_report_query
        self._describe_file_import_hotspots_query = describe_file_import_hotspots_query
        self._grouped_violation_view = grouped_violation_view
        self._file_import_hotspots_view = file_import_hotspots_view
        self._json_report_view = json_report_view
        self._check_summary_presenter = check_summary_presenter

    def register(self, app: click.Group) -> None:
        app.add_command(self.build_check_command())
        app.add_command(self.build_hotspots_command())

    def build_check_command(self) -> click.Command:
        return click.Command(
            name="check",
            help="Run architecture checks using the project config.",
            callback=self._invoke_check_command,
            params=cast(list[click.Parameter], [
                click.Option(["--project-root"], default=".",
                             show_default=True, help="Project root to analyze"),
                click.Option(["--config"], default=None,
                             help="Optional config path"),
                click.Option(["--output", "output_format"], type=click.Choice(
                    ["text", "json"]), default="text", show_default=True, help="Output format"),
                click.Option(["--dot", "dot_path"], default=None,
                             help="Optional path to write a DOT graph for violating paths"),
            ]),
        )

    def _invoke_check_command(self, project_root: str, config: str | None, output_format: str, dot_path: str | None) -> int:
        return self.run_check(project_root, config, output_format, dot_path)

    def build_hotspots_command(self) -> click.Command:
        return click.Command(
            name="hotspots",
            help="Show file import hotspot counts using the dependency graph.",
            callback=self._invoke_hotspots_command,
            params=cast(list[click.Parameter], [
                click.Option(["--project-root"], default=".",
                             show_default=True, help="Project root to analyze"),
                click.Option(["--config"], default=None,
                             help="Optional config path"),
                click.Option(["--sort-by"], type=click.Choice(
                    ["imported_by_count", "imports_count"]), default="imported_by_count", show_default=True, help="Metric to sort by"),
                click.Option(["--descending/--ascending"], default=True,
                             show_default=True, help="Sort order"),
                click.Option(["--output", "output_format"], type=click.Choice(
                    ["text", "json"]), default="text", show_default=True, help="Output format"),
            ]),
        )

    def _invoke_hotspots_command(
        self,
        project_root: str,
        config: str | None,
        sort_by: str,
        descending: bool,
        output_format: str,
    ) -> int:
        return self.run_hotspots(
            project_root,
            config,
            sort_by,
            descending,
            output_format,
        )

    def run_check(self, project_root: str, config: str | None, output_format: str, dot_path: str | None) -> int:
        report = self._build_architecture_report_query.execute(
            Path(project_root).expanduser().resolve(),
            config,
        )

        if report.check_error is not None:
            if output_format == "json":
                click.echo(self._json_report_view.render(
                    report.to_json_dict()))
                return 1
            click.echo(f"Error: {report.check_error}")
            return 1

        if dot_path is not None:
            Path(dot_path).expanduser().resolve().write_text(
                report.dot_report, encoding="utf-8")

        if output_format == "json":
            click.echo(self._json_report_view.render(report.to_json_dict()))
            return 1 if report.violations else 0

        click.echo(
            self._check_summary_presenter.render(
                report.files_found,
                report.files_excluded,
                report.files_checked,
            )
        )

        if report.violations:
            click.echo("\n=== Architectural Violations Detected ===")
            click.echo(
                self._grouped_violation_view.render(
                    report.violation_groups
                )
            )
            if dot_path is not None:
                click.echo(
                    f"Wrote DOT report to {Path(dot_path).expanduser().resolve()}")
            return 1

        if dot_path is not None:
            click.echo(
                f"Wrote DOT report to {Path(dot_path).expanduser().resolve()}")
        click.echo("Architecture Check Passed! No violations found.")
        return 0

    def run_hotspots(
        self,
        project_root: str,
        config: str | None,
        sort_by: str,
        descending: bool,
        output_format: str,
    ) -> int:
        result = self._describe_file_import_hotspots_query.describe(
            Path(project_root).expanduser().resolve(),
            config,
            sort_by=cast(FileImportHotspotsSortBy, sort_by),
            descending=descending,
        )

        if output_format == "json":
            click.echo(self._json_report_view.render(result.to_json_dict()))
            return 0

        click.echo(self._file_import_hotspots_view.render(result))
        return 0


__all__ = ["ArchitectureCheckCli"]
