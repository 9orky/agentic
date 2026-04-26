from __future__ import annotations

from pathlib import Path

import click
from agentic.project_layout import AgenticProjectLayout

from ..application import describe_recipe_generation, generate_recipe, load_code_generation_settings
from .views import build_default_code_generation_view


@click.command(name="code")
@click.argument("recipe_name")
@click.argument("path", required=False, default=".")
@click.option("--dry-run", is_flag=True, help="Show what would be created without changing files")
@click.pass_context
def _code_command(ctx: click.Context, recipe_name: str, path: str, dry_run: bool) -> int:
    runtime = ctx.obj
    project_root = runtime.resolve_project_root(".")
    target_path = Path(path)
    view = build_default_code_generation_view()
    layout = AgenticProjectLayout()
    try:
        recipe_root = _resolve_recipe_root(project_root, layout=layout)
        code_config = load_code_generation_settings(
            project_root=project_root,
            config_candidate_paths=layout.config_candidate_paths,
        )
        recipe_root_label = _present_path(
            recipe_root, project_root=project_root)
    except ValueError as exc:
        raise click.ClickException(str(exc)) from exc

    if dry_run:
        try:
            result = describe_recipe_generation(
                recipe_name,
                project_root,
                target_path,
                recipe_root=recipe_root,
                config=code_config,
            )
        except ValueError as exc:
            raise click.ClickException(str(exc)) from exc
        for line in view.render_dry_run_result(
            result,
            project_root=project_root,
            recipe_root_label=recipe_root_label,
        ):
            click.echo(line)
        if not result["recipe_found"]:
            ctx.exit(1)
        return 0

    try:
        result = generate_recipe(
            recipe_name,
            project_root,
            target_path,
            recipe_root=recipe_root,
            config=code_config,
        )
    except ValueError as exc:
        raise click.ClickException(str(exc)) from exc
    for line in view.render_generate_result(
        result,
        project_root=project_root,
        recipe_root_label=recipe_root_label,
    ):
        click.echo(line)
    if not result["recipe_found"]:
        ctx.exit(1)
    return 0


def _present_path(path: Path, *, project_root: Path) -> str:
    try:
        return path.relative_to(project_root).as_posix()
    except ValueError:
        return str(path)


def _resolve_recipe_root(project_root: Path, *, layout: AgenticProjectLayout) -> Path:
    target_root = project_root.resolve()

    for candidate in (target_root, *target_root.parents):
        code_dir = layout.target_dir(candidate) / "code"
        if code_dir.is_dir():
            return code_dir

        config_path = layout.config_path(candidate)
        if config_path.is_file():
            return config_path.parent / "code"

    return layout.target_dir(target_root) / "code"


def code_cli(app: click.Group) -> None:
    app.add_command(_code_command)


__all__ = ["code_cli"]
