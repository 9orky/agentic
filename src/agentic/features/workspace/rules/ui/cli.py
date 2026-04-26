from __future__ import annotations

import click
from agentic.cli_support import echo_lines

from ..application import build_rule_schema_report
from .views import build_default_rule_schema_report_view


def _render_rule_schema_report() -> int:
    report = build_rule_schema_report()
    echo_lines(build_default_rule_schema_report_view().render(report))
    return 1 if report.has_findings else 0


@click.command(
    name="check-rules",
    help="Validate the packaged rule markdown corpus and report structural issues.",
)
def _check_rules_command() -> int:
    return _render_rule_schema_report()


@click.command(
    name="check-rule-schema",
    help="Alias for check-rules.",
)
def _check_rule_schema_command() -> int:
    return _render_rule_schema_report()


def rule_schema_cli(app: click.Group) -> None:
    app.add_command(_check_rules_command)
    app.add_command(_check_rule_schema_command)


__all__ = ["rule_schema_cli"]
