from __future__ import annotations

import click

from .features.architecture_check.cli import architecture_check_cli
from .features.configuration.cli import configuration_cli
from .features.llm_handoff.cli import llm_handoff_cli
from .features.workspace_contract.cli import workspace_contract_cli


@click.group(name="agentic", invoke_without_command=True)
@click.option("--llm", is_flag=True, help="Print the handoff prompt for the user's LLM")
@click.pass_context
def agentic_cli(ctx: click.Context, llm: bool) -> int | None:
    """Compose feature-owned CLI apps for agentic."""
    if ctx.invoked_subcommand is not None:
        return None

    if llm:
        return ctx.invoke(agentic_cli.commands["llm"], project_root=".")

    return ctx.invoke(agentic_cli.commands["init"], project_root=".")


@agentic_cli.command("help")
@click.pass_context
def help_command(ctx: click.Context) -> int:
    """Show the command summary and available options."""
    parent = ctx.parent
    if parent is not None:
        click.echo(parent.get_help())
    return 0


workspace_contract_cli(agentic_cli)
configuration_cli(agentic_cli)
architecture_check_cli(agentic_cli)
llm_handoff_cli(agentic_cli)


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

    if result is None:
        return 0
    return int(result)
