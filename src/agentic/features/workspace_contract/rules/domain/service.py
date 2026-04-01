from __future__ import annotations

from pathlib import Path, PurePosixPath
from posixpath import normpath

from .entity import RuleDocument, RuleDocumentCheck, RuleDocumentFile, RuleDocumentSchema
from .value_object import RuleDocumentClass, RuleReference, RuleSchemaViolation, RuleSectionRequirement


class RuleSchemaPolicy:
    def __init__(
        self,
        *,
        navigational_schema: RuleDocumentSchema | None = None,
        policy_schema: RuleDocumentSchema | None = None,
        execution_big_picture_schema: RuleDocumentSchema | None = None,
        execution_step_schema: RuleDocumentSchema | None = None,
    ) -> None:
        self._navigational_schema = navigational_schema or RuleDocumentSchema.navigational()
        self._policy_schema = policy_schema or RuleDocumentSchema.policy()
        self._execution_big_picture_schema = execution_big_picture_schema or RuleDocumentSchema.execution_big_picture()
        self._execution_step_schema = execution_step_schema or RuleDocumentSchema.execution_step()

    def schema_for(self, document_class: RuleDocumentClass, *, stage: str | None = None) -> RuleDocumentSchema:
        if document_class is RuleDocumentClass.NAVIGATIONAL:
            return self._navigational_schema
        if document_class is RuleDocumentClass.POLICY:
            return self._policy_schema
        if stage == "big_picture":
            return self._execution_big_picture_schema
        return self._execution_step_schema

    def validate_document(
        self,
        *,
        document_class: RuleDocumentClass,
        observed_section_headings: tuple[str, ...],
        has_navigation_targets: bool,
        stage: str | None = None,
    ) -> tuple[RuleSchemaViolation, ...]:
        schema = self.schema_for(document_class, stage=stage)
        violations = list(
            self._validate_requirements(
                observed_headings=observed_section_headings,
                requirements=schema.section_requirements,
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

    def inspect_document(self, document_file: RuleDocumentFile) -> RuleDocumentCheck:
        document = RuleDocument.from_file(document_file)
        return RuleDocumentCheck(
            document=document,
            violations=self.validate_document(
                document_class=document.document_class,
                observed_section_headings=document.observed_section_headings,
                has_navigation_targets=document.has_navigation_targets,
                stage=document.stage,
            ),
        )

    def validate_references(
        self,
        *,
        document: RuleDocument,
        known_paths: set[Path],
    ) -> tuple[RuleSchemaViolation, ...]:
        violations: list[RuleSchemaViolation] = []

        for reference in document.references:
            resolved_path = self._resolve_reference_path(reference)
            if resolved_path is None:
                violations.append(
                    RuleSchemaViolation(
                        code="invalid-reference-path",
                        message="Rule metadata reference must resolve to a markdown rule document inside the packaged rules tree",
                        reference_path=reference.raw_path,
                    )
                )
                continue

            if resolved_path not in known_paths:
                violations.append(
                    RuleSchemaViolation(
                        code="missing-reference-target",
                        message="Rule metadata reference does not point to a packaged rule document",
                        reference_path=reference.raw_path,
                    )
                )

        return tuple(violations)

    def _validate_requirements(
        self,
        *,
        observed_headings: tuple[str, ...],
        requirements: tuple[RuleSectionRequirement, ...],
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
                section_positions=positions,
                invalid_order_code=invalid_order_code,
                invalid_order_message_prefix=invalid_order_message_prefix,
            )
        )
        return tuple(violations)

    @staticmethod
    def _find_heading_index(
        observed_headings: tuple[str, ...],
        requirement: RuleSectionRequirement,
    ) -> int | None:
        for index, heading in enumerate(observed_headings):
            if requirement.matches(heading):
                return index
        return None

    @staticmethod
    def _ordering_violations(
        *,
        section_positions: list[tuple[int, str]],
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
                        message=(
                            f"{invalid_order_message_prefix}: {current_heading} "
                            f"appears before {previous_heading}"
                        ),
                        section_heading=current_heading,
                    )
                )

        return tuple(violations)

    @staticmethod
    def _resolve_reference_path(reference: RuleReference) -> Path | None:
        base_path = PurePosixPath(reference.source_path.as_posix()).parent
        normalized_reference = normpath(
            str(base_path.joinpath(reference.raw_path)))
        resolved_path = PurePosixPath(normalized_reference)

        if str(resolved_path) == ".":
            return None
        if resolved_path.is_absolute():
            return None
        if resolved_path.suffix != ".md":
            return None
        if any(part == ".." for part in resolved_path.parts):
            return None

        return Path(str(resolved_path))


__all__ = ["RuleSchemaPolicy"]
