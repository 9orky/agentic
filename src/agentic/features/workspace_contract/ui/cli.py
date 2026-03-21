from __future__ import annotations

from pathlib import Path

import click

from .. import BootstrapError
from ..application import BootstrapProject, UpdateProject
from .views import SyncSummaryView

__all__ = ["workspace_contract_cli"]


@click.command(name="init")
@click.option("--project-root", default=".", show_default=True, help="Project root to bootstrap")
def _init_command(project_root: str) -> int:
    try:
        resolved_project_root = Path(project_root).expanduser().resolve()
        result = BootstrapProject().execute(resolved_project_root)
    except BootstrapError as exc:
        click.echo(f"Error: {exc}")
        return 1
    except NotADirectoryError as exc:
        click.echo(f"Error: {exc}")
        return 1

    for line in SyncSummaryView().render_bootstrap_result(result, project_root=resolved_project_root):
        click.echo(line)
    return 0


@click.command(name="update")
@click.option("--project-root", default=".", show_default=True, help="Project root to update")
def _update_command(project_root: str) -> int:
    try:
        resolved_project_root = Path(project_root).expanduser().resolve()
        result = UpdateProject().execute(resolved_project_root)
    except BootstrapError as exc:
        click.echo(f"Error: {exc}")
        return 1
    except NotADirectoryError as exc:
        click.echo(f"Error: {exc}")
        return 1

    for line in SyncSummaryView().render_update_result(result, project_root=resolved_project_root):
        click.echo(line)
    return 0


def workspace_contract_cli(app: click.Group) -> None:
    app.add_command(_init_command)
    app.add_command(_update_command)