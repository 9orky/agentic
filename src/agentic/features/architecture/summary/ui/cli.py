from __future__ import annotations

import click

from agentic.cli_support import config_option, output_option, project_root_option, render_json

from ..application import describe_architecture_summary
from .views import ArchitectureSummaryView


def _summary_to_json(report) -> dict[str, object]:
    return {
        "sections": [
            {
                "title": section.title,
                "entries": list(section.entries),
            }
            for section in report.sections
        ],
        "reading_priorities": [
            {
                "path": entry.path,
                "reason": entry.reason,
                "risk_level": entry.risk_level,
            }
            for entry in report.reading_priorities
        ],
        "risk_findings": [
            {
                "path": finding.path,
                "summary": finding.summary,
                "risk_level": finding.risk_level,
            }
            for finding in report.risk_findings
        ],
    }


@click.command(
    name="summary",
    help=(
        "Summarize the repository for an agent: what to read first, where the "
        "architectural pressure lives, and which files deserve extra care."
    ),
)
@project_root_option(help_text="Project root whose source tree should be analyzed.")
@config_option(help_text="Use a specific architecture config file instead of auto-discovery.")
@click.option(
    "--top",
    type=click.IntRange(1, 50),
    default=10,
    show_default=True,
    help="Limit how many high-signal files appear in the summary sections.",
)
@output_option()
@click.pass_obj
def _summary_command(
    runtime,
    project_root: str,
    config: str | None,
    top: int,
    output_format: str,
) -> int:
    report = describe_architecture_summary(
        runtime.resolve_project_root(project_root),
        config,
        top=top,
    )

    if output_format == "json":
        click.echo(render_json(_summary_to_json(report)))
        return 0

    click.echo(ArchitectureSummaryView().render(report))
    return 0


def summary_cli(app: click.Group) -> None:
    app.add_command(_summary_command)


__all__ = ["summary_cli"]
