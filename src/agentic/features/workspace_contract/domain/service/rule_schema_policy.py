from __future__ import annotations

from dataclasses import dataclass, field

from ..value_object import RuleDocumentClass, RuleDocumentSchema, RuleSchemaViolation


@dataclass(frozen=True)
class RuleSchemaPolicy:
    navigational_schema: RuleDocumentSchema = field(
        default_factory=RuleDocumentSchema.navigational)
    leaf_schema: RuleDocumentSchema = field(
        default_factory=RuleDocumentSchema.leaf)

    def schema_for(self, document_class: RuleDocumentClass) -> RuleDocumentSchema:
        if document_class is RuleDocumentClass.NAVIGATIONAL:
            return self.navigational_schema
        return self.leaf_schema

    def validate_document(
        self,
        *,
        document_class: RuleDocumentClass,
        observed_section_headings: tuple[str, ...],
        has_navigation_targets: bool,
    ) -> tuple[RuleSchemaViolation, ...]:
        schema = self.schema_for(document_class)
        violations: list[RuleSchemaViolation] = []
        violations.extend(
            self._validate_requirements(
                observed_section_headings,
                schema.section_requirements,
                missing_code="missing-section",
                invalid_order_code="invalid-section-order",
                missing_message_prefix="Missing required section",
                invalid_order_message_prefix="Section order is invalid",
            )
        )

        if schema.navigation_targets_required and not has_navigation_targets:
            violations.append(
                RuleSchemaViolation(
                    code="missing-navigation-targets",
                    message="Navigational documents must declare at least one navigation target",
                )
            )

        return tuple(violations)

    def _validate_requirements(
        self,
        observed_headings: tuple[str, ...],
        requirements,
        *,
        missing_code: str,
        invalid_order_code: str,
        missing_message_prefix: str,
        invalid_order_message_prefix: str,
    ) -> tuple[RuleSchemaViolation, ...]:
        violations: list[RuleSchemaViolation] = []
        positions: list[tuple[int, str]] = []

        for requirement in requirements:
            matched_index = self._find_heading_index(
                observed_headings, requirement)
            if matched_index is None:
                if requirement.required:
                    violations.append(
                        RuleSchemaViolation(
                            code=missing_code,
                            message=f"{missing_message_prefix}: {requirement.canonical_heading}",
                            section_heading=requirement.canonical_heading,
                        )
                    )
                continue
            positions.append((matched_index, requirement.canonical_heading))

        violations.extend(
            self._ordering_violations(
                positions,
                invalid_order_code=invalid_order_code,
                invalid_order_message_prefix=invalid_order_message_prefix,
            )
        )
        return tuple(violations)

    @staticmethod
    def _find_heading_index(observed_headings: tuple[str, ...], requirement) -> int | None:
        for index, heading in enumerate(observed_headings):
            if requirement.matches(heading):
                return index
        return None

    @staticmethod
    def _ordering_violations(
        section_positions: list[tuple[int, str]],
        *,
        invalid_order_code: str,
        invalid_order_message_prefix: str,
    ) -> tuple[RuleSchemaViolation, ...]:
        violations: list[RuleSchemaViolation] = []

        for current_index in range(1, len(section_positions)):
            previous_position, previous_heading = section_positions[current_index - 1]
            current_position, current_heading = section_positions[current_index]
            if current_position < previous_position:
                violations.append(
                    RuleSchemaViolation(
                        code=invalid_order_code,
                        message=f"{invalid_order_message_prefix}: {current_heading} appears before {previous_heading}",
                        section_heading=current_heading,
                    )
                )

        return tuple(violations)
