from __future__ import annotations

from dataclasses import dataclass


class CheckerError(RuntimeError):
    pass


@dataclass(frozen=True)
class ViolationGroup:
    title: str
    entries: tuple[str, ...]


__all__ = ["CheckerError", "ViolationGroup"]
