from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import click

from .features.architecture_check.cli import architecture_check_cli
from .features.workspace.cli import workspace_contract_cli


@dataclass(frozen=True)
class AgenticCliRuntime:
    cwd: Path

    def resolve_project_root(self, project_root: str) -> Path:
        requested_root = Path(project_root).expanduser()
        if requested_root.is_absolute():
            return requested_root.resolve()

        return (self.cwd / requested_root).resolve()


def build_cli_runtime(*, cwd: Path | None = None) -> AgenticCliRuntime:
    runtime_cwd = (cwd or Path.cwd()).expanduser().resolve()
    return AgenticCliRuntime(cwd=runtime_cwd)


@click.group(name="agentic", invoke_without_command=True)
@click.pass_context
def agentic_cli(ctx: click.Context) -> int | None:
    ctx.obj = build_cli_runtime()
    if ctx.invoked_subcommand is not None:
        return None

    return ctx.invoke(agentic_cli.commands["init"], project_root=".")


@agentic_cli.command("help")
@click.pass_context
def help_command(ctx: click.Context) -> int:
    parent = ctx.parent
    if parent is not None:
        click.echo(parent.get_help())
    return 0


workspace_contract_cli(agentic_cli)
architecture_check_cli(agentic_cli)


def main(argv: list[str] | None = None) -> int:
    try:
        result = agentic_cli.main(
            args=argv,
            prog_name="agentic",
            standalone_mode=False,
        )
    except click.exceptions.Exit as exc:
        return exc.exit_code
    except click.ClickException as exc:
        exc.show()
        return exc.exit_code
    except click.Abort:
        click.echo("Aborted!", err=True)
        return 1
    except Exception as exc:
        click.echo(f"Error: {exc}", err=True)
        return 1

    if result is None:
        return 0
    return int(result)


__all__ = ["AgenticCliRuntime", "agentic_cli", "build_cli_runtime", "main"]
