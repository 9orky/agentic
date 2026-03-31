from __future__ import annotations

from dataclasses import dataclass

from .rule_document_class import RuleDocumentClass
from .rule_section_requirement import RuleSectionRequirement


@dataclass(frozen=True)
class RuleDocumentSchema:
    document_class: RuleDocumentClass
    section_requirements: tuple[RuleSectionRequirement, ...]
    navigation_targets_required: bool = False

    def __post_init__(self) -> None:
        if not self.section_requirements:
            raise ValueError(
                "Rule document schemas must declare at least one section requirement")

    @classmethod
    def navigational(cls) -> RuleDocumentSchema:
        return cls(
            document_class=RuleDocumentClass.NAVIGATIONAL,
            section_requirements=(
                RuleSectionRequirement(("Purpose",)),
                RuleSectionRequirement(("Use This When",)),
                RuleSectionRequirement(("Available Options",)),
                RuleSectionRequirement(("Navigation Rule",)),
                RuleSectionRequirement(("Local Context",), required=False),
                RuleSectionRequirement(("Exit Condition",)),
            ),
            navigation_targets_required=True,
        )

    @classmethod
    def leaf(cls) -> RuleDocumentSchema:
        return cls(
            document_class=RuleDocumentClass.LEAF,
            section_requirements=(
                RuleSectionRequirement(("Purpose",)),
                RuleSectionRequirement(("Applies When",)),
                RuleSectionRequirement(("Ownership", "Scope")),
                RuleSectionRequirement(("Core Rules",)),
                RuleSectionRequirement(("Constraints",)),
                RuleSectionRequirement(
                    ("If Ambiguous, Go To",), required=False),
                RuleSectionRequirement(("Acceptance Check",)),
            ),
        )

    def required_sections(self) -> tuple[RuleSectionRequirement, ...]:
        return tuple(requirement for requirement in self.section_requirements if requirement.required)
