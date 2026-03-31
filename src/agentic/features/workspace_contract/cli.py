from __future__ import annotations

import click

from .rules import rule_schema_cli as register_rule_schema_cli
from .sync import sync_cli

__all__ = ["workspace_contract_cli"]


def workspace_contract_cli(app: click.Group) -> None:
    sync_cli(app)
    register_rule_schema_cli(app)
