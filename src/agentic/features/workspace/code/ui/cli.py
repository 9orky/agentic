from __future__ import annotations

import click

from ..application import describe_recipe_generation, generate_recipe
from .views import build_default_code_generation_view


@click.command(name="code")
@click.argument("recipe_name")
@click.option("--dry-run", is_flag=True, help="Show what would be created without changing files")
@click.pass_context
def _code_command(ctx: click.Context, recipe_name: str, dry_run: bool) -> int:
    runtime = ctx.obj
    project_root = runtime.resolve_project_root(".")
    view = build_default_code_generation_view()

    if dry_run:
        result = describe_recipe_generation(recipe_name, project_root)
        for line in view.render_dry_run_result(result, project_root=project_root):
            click.echo(line)
        if not result["recipe_found"]:
            ctx.exit(1)
        return 0

    result = generate_recipe(recipe_name, project_root)
    for line in view.render_generate_result(result, project_root=project_root):
        click.echo(line)
    if not result["recipe_found"]:
        ctx.exit(1)
    return 0


def code_cli(app: click.Group) -> None:
    app.add_command(_code_command)


__all__ = ["code_cli"]
