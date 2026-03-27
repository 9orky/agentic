from __future__ import annotations

import click

from .checker.ui import architecture_check_cli as register_architecture_check_cli


def architecture_check_cli(app: click.Group) -> None:
    register_architecture_check_cli(app)


__all__ = ["architecture_check_cli"]
