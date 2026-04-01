from __future__ import annotations

import re
from posixpath import normpath
from pathlib import Path
from typing import Literal, Self

import yaml
from pydantic import BaseModel, ConfigDict, TypeAdapter, ValidationError, model_validator

from .value_object import RuleDocumentClass, RuleDocumentParseError, RuleReference, RuleSchemaViolation, RuleSectionRequirement

_FRONTMATTER_PATTERN = re.compile(
    r"\A---\s*\n(?P<value>.*?)\n---\s*(?:\n|\Z)", re.DOTALL)
_SECTION_HEADING_PATTERN = re.compile(r"^##\s+(?P<value>.+)$", re.MULTILINE)
_MARKDOWN_LINK_PATTERN = re.compile(r"\[[^\]]+\]\([^)]+\)")


class RuleDocumentFile(BaseModel):
    model_config = ConfigDict(frozen=True)

    path: Path
    content: str

    @model_validator(mode="after")
    def validate_document(self) -> Self:
        if self.path.suffix != ".md":
            raise ValueError("Rule document files must be markdown documents")
        if not self.content.strip():
            raise ValueError("Rule document files must not be empty")
        return self


class NavigationalRuleDocumentMetadata(BaseModel):
    model_config = ConfigDict(frozen=True)

    doc_class: Literal["navigational"]
    rule_kind: Literal["navigation"]
    audience: str
    purpose: str
    applies_when: tuple[str, ...]
    tags: tuple[str, ...]
    read_directly: bool
    entrypoint: bool
    read_strategy: str
    child_paths: tuple[str, ...]


class PolicyRuleDocumentMetadata(BaseModel):
    model_config = ConfigDict(frozen=True)

    doc_class: Literal["policy"]
    rule_kind: Literal["policy"]
    audience: str
    purpose: str
    applies_when: tuple[str, ...]
    tags: tuple[str, ...]
    read_directly: bool
    scope: str = "shared"
    tightens_paths: tuple[str, ...] = ()
    escalation_paths: tuple[str, ...] = ()


class ExecutionRuleDocumentMetadata(BaseModel):
    model_config = ConfigDict(frozen=True)

    doc_class: Literal["execution"]
    rule_kind: Literal["execution"]
    audience: str
    purpose: str
    applies_when: tuple[str, ...]
    tags: tuple[str, ...]
    read_directly: bool
    stage: Literal["big_picture", "step"]
    same_artifact_family: str
    scope: str = "shared"
    tightens_paths: tuple[str, ...] = ()
    escalation_paths: tuple[str, ...] = ()


_RULE_DOCUMENT_METADATA_ADAPTER = TypeAdapter(
    NavigationalRuleDocumentMetadata | PolicyRuleDocumentMetadata | ExecutionRuleDocumentMetadata
)


class RuleDocument(BaseModel):
    model_config = ConfigDict(frozen=True)

    path: Path
    document_class: RuleDocumentClass
    stage: str | None = None
    observed_section_headings: tuple[str, ...]
    has_navigation_targets: bool
    references: tuple[RuleReference, ...] = ()

    @classmethod
    def from_file(cls, document_file: RuleDocumentFile) -> RuleDocument:
        metadata = _metadata_from(document_file.content)
        return cls(
            path=document_file.path,
            document_class=RuleDocumentClass.from_literal(metadata.doc_class),
            stage=getattr(metadata, "stage", None),
            observed_section_headings=_section_headings_from(
                document_file.content),
            has_navigation_targets=_has_navigation_targets(
                document_file.content, metadata),
            references=_references_from(document_file.path, metadata),
        )


class RuleDocumentCheck(BaseModel):
    model_config = ConfigDict(frozen=True)

    document: RuleDocument
    violations: tuple[RuleSchemaViolation, ...]


class RuleDocumentSchema(BaseModel):
    model_config = ConfigDict(frozen=True)

    document_class: RuleDocumentClass
    section_requirements: tuple[RuleSectionRequirement, ...]
    navigation_targets_required: bool = False

    @model_validator(mode="after")
    def validate_section_requirements(self) -> Self:
        if not self.section_requirements:
            raise ValueError(
                "Rule document schemas must declare at least one section requirement"
            )
        return self

    @classmethod
    def navigational(cls) -> RuleDocumentSchema:
        return cls(
            document_class=RuleDocumentClass.NAVIGATIONAL,
            section_requirements=(
                RuleSectionRequirement(
                    headings=("Use This Branch When",), required=False),
                RuleSectionRequirement(headings=("Stop Or Descend",)),
                RuleSectionRequirement(headings=("Branches",), required=False),
                RuleSectionRequirement(headings=("Review Checks",)),
            ),
            navigation_targets_required=True,
        )

    @classmethod
    def policy(cls) -> RuleDocumentSchema:
        return cls(
            document_class=RuleDocumentClass.POLICY,
            section_requirements=(
                RuleSectionRequirement(headings=("Required Decisions",)),
                RuleSectionRequirement(headings=("Core Rules",)),
                RuleSectionRequirement(
                    headings=("Layer Starter Rules",), required=False),
                RuleSectionRequirement(headings=("Review Checks",)),
            ),
        )

    @classmethod
    def execution_big_picture(cls) -> RuleDocumentSchema:
        return cls(
            document_class=RuleDocumentClass.EXECUTION,
            section_requirements=(
                RuleSectionRequirement(headings=("Required Sections",)),
                RuleSectionRequirement(
                    headings=("Optional Sections",), required=False),
                RuleSectionRequirement(headings=("File Tree Rules",)),
                RuleSectionRequirement(headings=("Phase Rules",)),
                RuleSectionRequirement(
                    headings=("Strategic Model Gate",), required=False),
                RuleSectionRequirement(headings=("Review Checks",)),
                RuleSectionRequirement(headings=("Handoff Checks",)),
            ),
        )

    @classmethod
    def execution_step(cls) -> RuleDocumentSchema:
        return cls(
            document_class=RuleDocumentClass.EXECUTION,
            section_requirements=(
                RuleSectionRequirement(headings=("Required Sections",)),
                RuleSectionRequirement(
                    headings=("Implementation Tree Rules",)),
                RuleSectionRequirement(headings=("Step Contract Rules",)),
                RuleSectionRequirement(headings=("Execution Rules",)),
                RuleSectionRequirement(headings=("Review Checks",)),
                RuleSectionRequirement(headings=("Handoff Checks",)),
            ),
        )

    def required_sections(self) -> tuple[RuleSectionRequirement, ...]:
        return tuple(
            requirement
            for requirement in self.section_requirements
            if requirement.required
        )


def _metadata_from(content: str) -> NavigationalRuleDocumentMetadata | PolicyRuleDocumentMetadata | ExecutionRuleDocumentMetadata:
    match = _FRONTMATTER_PATTERN.match(content)
    if match is None:
        raise RuleDocumentParseError(
            "Rule document must declare YAML frontmatter")

    payload = yaml.safe_load(match.group("value"))
    if not isinstance(payload, dict):
        raise RuleDocumentParseError(
            "Rule document frontmatter must be a mapping")

    try:
        return _RULE_DOCUMENT_METADATA_ADAPTER.validate_python(payload)
    except ValidationError as exc:
        first_error = exc.errors()[0]["msg"]
        raise RuleDocumentParseError(
            f"Invalid rule document frontmatter: {first_error}"
        ) from exc


def _section_headings_from(content: str) -> tuple[str, ...]:
    return tuple(
        match.group("value").strip()
        for match in _SECTION_HEADING_PATTERN.finditer(content)
    )


def _has_navigation_targets(
    content: str,
    metadata: NavigationalRuleDocumentMetadata | PolicyRuleDocumentMetadata | ExecutionRuleDocumentMetadata,
) -> bool:
    if isinstance(metadata, NavigationalRuleDocumentMetadata) and metadata.child_paths:
        return True
    return _MARKDOWN_LINK_PATTERN.search(content) is not None


def _references_from(
    document_path: Path,
    metadata: NavigationalRuleDocumentMetadata | PolicyRuleDocumentMetadata | ExecutionRuleDocumentMetadata,
) -> tuple[RuleReference, ...]:
    if isinstance(metadata, NavigationalRuleDocumentMetadata):
        raw_paths = metadata.child_paths
    else:
        raw_paths = metadata.tightens_paths + metadata.escalation_paths

    return tuple(
        RuleReference(
            source_path=document_path,
            raw_path=_normalize_reference_path(raw_path),
        )
        for raw_path in raw_paths
    )


def _normalize_reference_path(raw_path: str) -> str:
    normalized = normpath(raw_path.strip())
    return "." if normalized == "" else normalized


__all__ = [
    "RuleDocument",
    "RuleDocumentCheck",
    "RuleDocumentFile",
    "RuleDocumentSchema",
]
