from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RuleSchemaViolation:
    code: str
    message: str
    section_heading: str | None = None
