from __future__ import annotations

from pathlib import Path

import click

from . import CheckerError, run_architecture_check

__all__ = ["architecture_check_cli"]


def _print_check_summary(files_found: int, files_excluded: int, files_checked: int) -> None:
    click.echo("Check Summary:")
    click.echo(f"- Files found in scope: {files_found}")
    click.echo(f"- Files excluded by rules: {files_excluded}")
    click.echo(f"- Files checked: {files_checked}")


@click.command(name="check")
@click.option("--project-root", default=".", show_default=True, help="Project root to analyze")
@click.option("--config", default=None, help="Optional config path")
def _check_command(project_root: str, config: str | None) -> int:
    """Run architecture checks using the project config."""
    try:
        result = run_architecture_check(
            Path(project_root).expanduser().resolve(), config)
    except CheckerError as exc:
        click.echo(f"Error: {exc}")
        return 1

    _print_check_summary(result.files_found,
                         result.files_excluded, result.files_checked)

    if result.violations:
        click.echo("\n=== Architectural Violations Detected ===")
        click.echo("\n".join(result.violations))
        return 1

    click.echo("Architecture Check Passed! No violations found.")
    return 0


def architecture_check_cli(app: click.Group) -> None:
    app.add_command(_check_command)
