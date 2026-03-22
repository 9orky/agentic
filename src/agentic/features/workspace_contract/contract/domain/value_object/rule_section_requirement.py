from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RuleSectionRequirement:
    headings: tuple[str, ...]
    required: bool = True

    def __post_init__(self) -> None:
        normalized_headings = tuple(
            heading.strip()
            for heading in self.headings
            if heading.strip()
        )
        if not normalized_headings:
            raise ValueError(
                "Rule section requirements must declare at least one heading")

        object.__setattr__(self, "headings", normalized_headings)

    @property
    def canonical_heading(self) -> str:
        return self.headings[0]

    def matches(self, heading: str) -> bool:
        normalized_heading = heading.strip()
        return normalized_heading in self.headings
