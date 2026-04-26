from __future__ import annotations

import click

from agentic.cli_support import config_option, output_option, project_root_option, render_json

from ..application import describe_file_import_hotspots, explain_hotspot
from .views import FileImportHotspotsView, HotspotExplanationView


@click.command(
    name="hotspots",
    help=(
        "Rank files by architectural pressure so an agent can find risky, "
        "expensive parts of the graph before making edits."
    ),
)
@project_root_option(help_text="Project root whose source tree should be analyzed.")
@config_option(help_text="Use a specific architecture config file instead of auto-discovery.")
@click.option(
    "--sort-by",
    type=click.Choice(
        [
            "risk_score",
            "imported_by_count",
            "imports_count",
            "symbol_count",
            "public_symbol_count",
            "line_count",
        ]
    ),
    default="risk_score",
    show_default=True,
    help="Choose whether to rank by risk, dependency pressure, symbol surface, or file size.",
)
@click.option(
    "--descending/--ascending",
    default=True,
    show_default=True,
    help="Sort from highest to lowest counts, or invert the ranking.",
)
@click.option(
    "--top",
    type=click.IntRange(1, 100),
    default=20,
    show_default=True,
    help="Limit how many hotspot entries are shown.",
)
@click.option(
    "--explain",
    "explain_path",
    default=None,
    metavar="PATH",
    help="Explain why one tracked file is considered risky.",
)
@output_option()
@click.pass_obj
def _hotspots_command(
    runtime,
    project_root: str,
    config: str | None,
    sort_by: str,
    descending: bool,
    top: int,
    explain_path: str | None,
    output_format: str,
) -> int:
    resolved_project_root = runtime.resolve_project_root(project_root)
    result = describe_file_import_hotspots(
        resolved_project_root,
        config,
        sort_by=sort_by,
        descending=descending,
        top=top,
    )
    explanation = None
    if explain_path is not None:
        explanation = explain_hotspot(
            resolved_project_root,
            explain_path,
            config,
        )

    if output_format == "json":
        payload: dict[str, object] = {"hotspots": result.to_json_dict()}
        if explanation is not None:
            payload["explanation"] = explanation.to_json_dict()
        click.echo(render_json(payload))
        return 0

    click.echo(FileImportHotspotsView().render(result))
    if explanation is not None:
        click.echo("")
        click.echo(HotspotExplanationView().render(explanation))
    return 0


def hotspots_cli(app: click.Group) -> None:
    app.add_command(_hotspots_command)


__all__ = ["hotspots_cli"]
