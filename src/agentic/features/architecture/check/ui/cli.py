from __future__ import annotations

import click

from agentic.cli_support import (
    config_option,
    output_option,
    project_root_option,
    render_json,
    resolve_path,
)

from ..application import build_architecture_report
from .views import CheckSummaryPresenter, GroupedViolationView


@click.command(
    name="check",
    help=(
        "Validate the current project against the architecture agreement and "
        "report any boundary or flow violations."
    ),
)
@project_root_option(help_text="Project root whose source tree should be analyzed.")
@config_option(help_text="Use a specific architecture config file instead of auto-discovery.")
@output_option()
@click.option(
    "--dot",
    "dot_path",
    default=None,
    metavar="PATH",
    help="Write a DOT graph of violating paths to this file.",
)
@click.pass_obj
def _check_command(
    runtime,
    project_root: str,
    config: str | None,
    output_format: str,
    dot_path: str | None,
) -> int:
    report = build_architecture_report(
        runtime.resolve_project_root(project_root),
        config,
    )

    if report.check_error is not None:
        if output_format == "json":
            click.echo(render_json(report.to_json_dict()))
            return 1
        click.echo(f"Error: {report.check_error}")
        return 1

    resolved_dot_path = resolve_path(dot_path)
    if resolved_dot_path is not None:
        resolved_dot_path.write_text(report.dot_report, encoding="utf-8")

    if output_format == "json":
        click.echo(render_json(report.to_json_dict()))
        return 1 if report.violations else 0

    click.echo(
        CheckSummaryPresenter().render(
            report.files_found,
            report.files_excluded,
            report.files_checked,
        )
    )

    if report.violations:
        click.echo("\n=== Architectural Violations Detected ===")
        click.echo(GroupedViolationView().render(report.violation_groups))
        if resolved_dot_path is not None:
            click.echo(f"Wrote DOT report to {resolved_dot_path}")
        return 1

    if resolved_dot_path is not None:
        click.echo(f"Wrote DOT report to {resolved_dot_path}")
    click.echo("Architecture Check Passed! No violations found.")
    return 0


def check_cli(app: click.Group) -> None:
    app.add_command(_check_command)


__all__ = ["check_cli"]
