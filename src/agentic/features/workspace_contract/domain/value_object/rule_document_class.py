from __future__ import annotations

from enum import StrEnum


class RuleDocumentClass(StrEnum):
    NAVIGATIONAL = "navigational"
    LEAF = "leaf"

    @classmethod
    def from_literal(cls, value: str) -> RuleDocumentClass:
        normalized_value = value.strip().lower()
        return cls(normalized_value)
