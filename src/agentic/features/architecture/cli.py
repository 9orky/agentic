from __future__ import annotations

import click

from .check.ui import check_cli
from .hotspots.ui import hotspots_cli
from .summary.ui import summary_cli


@click.group(
    name="architecture",
    help=(
        "Inspect a repository's architecture agreement, dependency pressure, "
        "and agent-facing reading priorities."
    ),
)
def _architecture_group() -> None:
    pass


check_cli(_architecture_group)
hotspots_cli(_architecture_group)
summary_cli(_architecture_group)


def architecture_cli(app: click.Group) -> None:
    app.add_command(_architecture_group)


__all__ = ["architecture_cli"]
