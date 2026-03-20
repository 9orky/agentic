from __future__ import annotations

from pathlib import Path

import click

from ..architecture_check import CheckerError
from ..configuration import AgenticConfigError
from ..workspace_contract import BootstrapError, bootstrap_project
from .app.build_anchor_output import build_anchor_output
from . import build_llm_prompt

__all__ = ["llm_handoff_cli"]

_ANCHOR_NAMES = (
    "bootstrap",
    "rules",
    "config",
    "architecture",
    "update",
)


def _resolve_project_root(project_root: str) -> Path:
    return Path(project_root).expanduser().resolve()


def _bootstrap_project_root(project_root: str) -> Path:
    resolved_project_root = _resolve_project_root(project_root)
    bootstrap_project(resolved_project_root)
    return resolved_project_root


def _project_root_from_context(ctx: click.Context) -> Path:
    project_root = ctx.obj.get("project_root")
    if not isinstance(project_root, Path):
        raise click.ClickException("LLM project root was not initialized.")
    return project_root


def _config_path_from_context(ctx: click.Context) -> str | None:
    config_path = ctx.obj.get("config")
    if config_path is None or isinstance(config_path, str):
        return config_path
    raise click.ClickException("LLM config path was not initialized.")


@click.group(name="llm", invoke_without_command=True)
@click.option("--project-root", default=".", show_default=True, help="Project root to prepare for LLM handoff")
@click.option("--config", default=None, help="Optional config path for config and architecture anchors")
@click.pass_context
def _llm_command(ctx: click.Context, project_root: str, config: str | None) -> int | None:
    resolved_project_root = _resolve_project_root(project_root)

    ctx.obj = {"project_root": resolved_project_root, "config": config}

    if ctx.invoked_subcommand is None:
        try:
            resolved_project_root = _bootstrap_project_root(project_root)
        except BootstrapError as exc:
            click.echo(f"Error: {exc}")
            return 1
        click.echo(build_llm_prompt(resolved_project_root))
        return 0

    return None


def _build_anchor_command(anchor_name: str) -> click.Command:
    @click.command(name=anchor_name)
    @click.pass_context
    def _anchor_command(ctx: click.Context) -> int:
        project_root = _project_root_from_context(ctx)
        config_path = _config_path_from_context(ctx)
        try:
            click.echo(build_anchor_output(
                anchor_name, project_root, config_path))
        except (AgenticConfigError, BootstrapError, CheckerError) as exc:
            click.echo(f"Error: {exc}")
            return 1
        return 0

    return _anchor_command


def llm_handoff_cli(app: click.Group) -> None:
    app.add_command(_llm_command)
    for anchor_name in _ANCHOR_NAMES:
        _llm_command.add_command(_build_anchor_command(anchor_name))
