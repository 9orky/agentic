from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, ConfigDict, field_validator


class RuleDocumentParseError(ValueError):
    pass


class RuleDocumentClass(StrEnum):
    NAVIGATIONAL = "navigational"
    POLICY = "policy"
    EXECUTION = "execution"

    @classmethod
    def from_literal(cls, value: str) -> RuleDocumentClass:
        return cls(value.strip().lower())


class RuleSectionRequirement(BaseModel):
    model_config = ConfigDict(frozen=True)

    headings: tuple[str, ...]
    required: bool = True

    @field_validator("headings")
    @classmethod
    def validate_headings(cls, values: tuple[str, ...]) -> tuple[str, ...]:
        normalized = tuple(heading.strip()
                           for heading in values if heading.strip())
        if not normalized:
            raise ValueError(
                "Rule section requirements must declare at least one heading"
            )
        return normalized

    @property
    def canonical_heading(self) -> str:
        return self.headings[0]

    def matches(self, heading: str) -> bool:
        return heading.strip() in self.headings


class RuleSchemaViolation(BaseModel):
    model_config = ConfigDict(frozen=True)

    code: str
    message: str
    section_heading: str | None = None


__all__ = [
    "RuleDocumentClass",
    "RuleDocumentParseError",
    "RuleSchemaViolation",
    "RuleSectionRequirement",
]
