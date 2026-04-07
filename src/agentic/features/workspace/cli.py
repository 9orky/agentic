from __future__ import annotations

from importlib import import_module

import click

__all__ = ["workspace_contract_cli"]


def workspace_contract_cli(app: click.Group) -> None:
    import_module(".code.ui.cli", __package__).code_cli(app)
    import_module(".sync.ui.cli", __package__).sync_cli(app)
    import_module(".rules.ui.cli", __package__).rule_schema_cli(app)
