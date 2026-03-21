from __future__ import annotations

import click

from .ui import ArchitectureCheckCli


class ArchitectureCheckCliSeam:
    def __init__(self, ui_cli: ArchitectureCheckCli | None = None) -> None:
        self._ui_cli = ui_cli or ArchitectureCheckCli()

    def register(self, app: click.Group) -> None:
        self._ui_cli.register(app)


architecture_check_cli = ArchitectureCheckCliSeam().register

__all__ = ["ArchitectureCheckCliSeam", "architecture_check_cli"]
