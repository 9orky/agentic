from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ExtractorSpec:
    command: str
    resource_name: str
