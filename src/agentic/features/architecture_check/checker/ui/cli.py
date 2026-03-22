from __future__ import annotations

from pathlib import Path
from typing import cast

import click

from ..application import CheckerError
from ..application import build_architecture_report, build_dot_report, build_violation_groups
from .services import CheckSummaryPresenter
from .views import GroupedViolationView, JsonReportView


class ArchitectureCheckCli:
    def __init__(
        self,
        grouped_violation_view: GroupedViolationView | None = None,
        json_report_view: JsonReportView | None = None,
        check_summary_presenter: CheckSummaryPresenter | None = None,
    ) -> None:
        self._grouped_violation_view = grouped_violation_view or GroupedViolationView()
        self._json_report_view = json_report_view or JsonReportView()
        self._check_summary_presenter = check_summary_presenter or CheckSummaryPresenter()

    def register(self, app: click.Group) -> None:
        app.add_command(self.build_check_command())

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

    def run_check(self, project_root: str, config: str | None, output_format: str, dot_path: str | None) -> int:
        try:
            report = build_architecture_report(
                Path(project_root).expanduser().resolve(),
                config,
            )
        except CheckerError as exc:
            if output_format == "json":
                click.echo(f'{{"error": {exc.args[0]!r}}}')
                return 1
            click.echo(f"Error: {exc}")
            return 1

        if report.check_error is not None:
            if output_format == "json":
                click.echo(self._json_report_view.render(
                    report.to_json_dict()))
                return 1
            click.echo(f"Error: {report.check_error}")
            return 1

        if dot_path is not None:
            dot_text = build_dot_report(report)
            Path(dot_path).expanduser().resolve().write_text(
                dot_text, encoding="utf-8")

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
                    build_violation_groups(report)
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


architecture_check_cli = ArchitectureCheckCli().register

__all__ = ["ArchitectureCheckCli", "architecture_check_cli"]
