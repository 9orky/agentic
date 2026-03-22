from __future__ import annotations

import click

from .checker.ui import ArchitectureCheckCli


def architecture_check_cli(
    app: click.Group,
    ui_cli: ArchitectureCheckCli | None = None,
) -> None:
    (ui_cli or ArchitectureCheckCli()).register(app)


__all__ = ["architecture_check_cli"]
