from __future__ import annotations

import click
from agentic.cli_support import command_error_boundary, echo_lines, project_root_option

from ..application import bootstrap_project, update_project
from .views import build_default_sync_summary_view


@click.command(
    name="init",
    help="Create the project-local agentic contract in the target repository.",
)
@project_root_option(help_text="Project root where the agentic contract should be created.")
@click.pass_obj
@command_error_boundary(ValueError)
def _init_command(runtime, project_root: str) -> int:
    resolved_project_root = runtime.resolve_project_root(project_root)
    result = bootstrap_project(resolved_project_root)

    echo_lines(build_default_sync_summary_view().render_bootstrap_result(
        result,
        project_root=resolved_project_root,
    ))
    return 0


@click.command(
    name="update",
    help="Refresh packaged shared assets in an existing agentic contract.",
)
@project_root_option(help_text="Project root whose existing agentic contract should be refreshed.")
@click.pass_obj
@command_error_boundary(ValueError)
def _update_command(runtime, project_root: str) -> int:
    resolved_project_root = runtime.resolve_project_root(project_root)
    result = update_project(resolved_project_root)

    echo_lines(build_default_sync_summary_view().render_update_result(
        result,
        project_root=resolved_project_root,
    ))
    return 0


def sync_cli(app: click.Group) -> None:
    app.add_command(_init_command)
    app.add_command(_update_command)


__all__ = ["sync_cli"]
