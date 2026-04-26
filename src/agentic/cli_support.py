from __future__ import annotations

import json
from collections.abc import Callable, Iterable
from functools import wraps
from pathlib import Path
from typing import ParamSpec, TypeVar

import click

P = ParamSpec("P")
R = TypeVar("R")


def command_error_boundary(
    *error_types: type[BaseException],
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    handled_types = error_types or (ValueError,)

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @wraps(func)
        def wrapped(*args: P.args, **kwargs: P.kwargs) -> R:
            try:
                return func(*args, **kwargs)
            except handled_types as exc:
                raise click.ClickException(str(exc)) from exc

        return wrapped

    return decorator


def echo_lines(lines: Iterable[str]) -> None:
    for line in lines:
        click.echo(line)


def render_json(payload: object) -> str:
    return json.dumps(payload, indent=2, sort_keys=True)


def resolve_path(value: str | None) -> Path | None:
    if value is None:
        return None
    return Path(value).expanduser().resolve()


def project_root_option(*, help_text: str) -> Callable[[Callable[P, R]], Callable[P, R]]:
    return click.option(
        "--project-root",
        default=".",
        metavar="PATH",
        show_default=True,
        help=help_text,
    )


def config_option(*, help_text: str) -> Callable[[Callable[P, R]], Callable[P, R]]:
    return click.option(
        "--config",
        default=None,
        metavar="PATH",
        help=help_text,
    )


def output_option() -> Callable[[Callable[P, R]], Callable[P, R]]:
    return click.option(
        "--output",
        "output_format",
        type=click.Choice(["text", "json"]),
        default="text",
        show_default=True,
        help="Choose human-readable text or machine-readable JSON output.",
    )


__all__ = [
    "command_error_boundary",
    "config_option",
    "echo_lines",
    "output_option",
    "project_root_option",
    "render_json",
    "resolve_path",
]
