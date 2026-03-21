from __future__ import annotations

from pathlib import Path

import click

from . import BootstrapError, bootstrap_project, update_project

__all__ = ["workspace_contract_cli"]


def _print_bootstrap_message(result) -> None:
    status = "Created" if result.created_dir else "Found"
    click.echo(f"{status} {result.target_dir}.")
    if result.created_files:
        click.echo(f"Created {len(result.created_files)} file(s).")
    if result.preserved_files:
        click.echo(
            f"Preserved {len(result.preserved_files)} existing file(s).")
    click.echo("Safe to rerun: plain 'agentic' preserves existing local files.")
    click.echo("Next step: review agentic/agentic.yaml and run 'agentic check'.")


def _print_update_message(result) -> None:
    status = "Created" if result.created_dir else "Found"
    click.echo(f"{status} {result.target_dir}.")
    if result.created_files:
        click.echo(f"Created {len(result.created_files)} file(s).")
    if result.updated_files:
        click.echo(f"Updated {len(result.updated_files)} shared file(s).")
    if result.preserved_files:
        click.echo(
            f"Preserved {len(result.preserved_files)} existing file(s).")
    click.echo("Next step: review refreshed rules and run 'agentic check'.")


@click.command(name="init")
@click.option("--project-root", default=".", show_default=True, help="Project root to bootstrap")
def _init_command(project_root: str) -> int:
    """Create or validate the local agentic/ workspace contract."""
    try:
        result = bootstrap_project(Path(project_root).expanduser().resolve())
    except BootstrapError as exc:
        click.echo(f"Error: {exc}")
        return 1

    _print_bootstrap_message(result)
    return 0


@click.command(name="update")
@click.option("--project-root", default=".", show_default=True, help="Project root to update")
def _update_command(project_root: str) -> int:
    """Refresh shared workspace-contract docs in a project."""
    try:
        result = update_project(Path(project_root).expanduser().resolve())
    except BootstrapError as exc:
        click.echo(f"Error: {exc}")
        return 1

    _print_update_message(result)
    return 0


def workspace_contract_cli(app: click.Group) -> None:
    app.add_command(_init_command)
    app.add_command(_update_command)
