from __future__ import annotations

import click

from ..application import bootstrap_project, update_project
from .views import build_default_sync_summary_view


@click.command(name="init")
@click.option("--project-root", default=".", show_default=True, help="Project root to bootstrap")
@click.pass_obj
def _init_command(runtime, project_root: str) -> int:
    resolved_project_root = runtime.resolve_project_root(project_root)
    result = bootstrap_project(resolved_project_root)

    for line in build_default_sync_summary_view().render_bootstrap_result(
        result,
        project_root=resolved_project_root,
    ):
        click.echo(line)
    return 0


@click.command(name="update")
@click.option("--project-root", default=".", show_default=True, help="Project root to update")
@click.pass_obj
def _update_command(runtime, project_root: str) -> int:
    resolved_project_root = runtime.resolve_project_root(project_root)
    result = update_project(resolved_project_root)

    for line in build_default_sync_summary_view().render_update_result(
        result,
        project_root=resolved_project_root,
    ):
        click.echo(line)
    return 0


def sync_cli(app: click.Group) -> None:
    app.add_command(_init_command)
    app.add_command(_update_command)


__all__ = ["sync_cli"]
