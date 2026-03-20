from __future__ import annotations

from pathlib import Path

import click

from ..workspace_contract import BootstrapError, bootstrap_project
from . import build_llm_prompt

__all__ = ["llm_handoff_cli"]


@click.command(name="llm")
@click.option("--project-root", default=".", show_default=True, help="Project root to prepare for LLM handoff")
def _llm_command(project_root: str) -> int:
    resolved_project_root = Path(project_root).expanduser().resolve()
    try:
        bootstrap_project(resolved_project_root)
    except BootstrapError as exc:
        click.echo(f"Error: {exc}")
        return 1

    click.echo(build_llm_prompt(resolved_project_root))
    return 0


def llm_handoff_cli(app: click.Group) -> None:
    app.add_command(_llm_command)
