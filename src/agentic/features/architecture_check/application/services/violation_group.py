from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ViolationGroup:
    title: str
    entries: tuple[str, ...]
