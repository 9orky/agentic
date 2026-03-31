from __future__ import annotations

from typing import Annotated, Literal, TypeAlias

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


DocumentClass = Literal["navigational", "policy", "execution"]
RuleKind = Literal["navigation", "policy", "execution"]
ExecutionStage = Literal["big_picture", "step"]
Audience = Literal["agent", "human", "both"]
ReadStrategy = Literal["progressive", "direct"]
RuleScope = Literal["shared", "project"]
FieldValueKind = Literal[
    "text",
    "markdown",
    "boolean",
    "string_list",
    "path",
    "path_list",
    "link_list",
]
TreeKind = Literal["file", "implementation"]


def _clean_text(value: str) -> str:
    normalized = value.strip()
    if not normalized:
        raise ValueError("value must not be empty")
    return normalized


def _normalize_path(value: str) -> str:
    normalized = _clean_text(value)
    return normalized.replace("\\", "/")


def _clean_text_list(values: list[str]) -> list[str]:
    return [value.strip() for value in values if value.strip()]


class SchemaModel(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
        validate_assignment=True,
    )


class DocumentLink(SchemaModel):
    path: str
    label: str | None = None
    summary: str | None = None

    @field_validator("path")
    @classmethod
    def validate_path(cls, value: str) -> str:
        return _normalize_path(value)


class ChecklistItem(SchemaModel):
    key: str
    prompt: str
    expected: bool = True
    required: bool = True

    @field_validator("key", "prompt")
    @classmethod
    def validate_text(cls, value: str) -> str:
        return _clean_text(value)


class FieldTemplate(SchemaModel):
    key: str
    label: str
    value_kind: FieldValueKind = "text"
    required: bool = True
    repeatable: bool = False
    notes: str | None = None

    @field_validator("key", "label")
    @classmethod
    def validate_text(cls, value: str) -> str:
        return _clean_text(value)


class SectionTemplateBase(SchemaModel):
    key: str
    heading: str
    required: bool = True
    compact: bool = True
    notes: str | None = None

    @field_validator("key", "heading")
    @classmethod
    def validate_text(cls, value: str) -> str:
        return _clean_text(value)


class ProseSectionTemplate(SectionTemplateBase):
    section_kind: Literal["prose"] = "prose"
    guidance: list[str] = Field(default_factory=list)

    @field_validator("guidance")
    @classmethod
    def validate_guidance(cls, values: list[str]) -> list[str]:
        return _clean_text_list(values)


class ChecklistSectionTemplate(SectionTemplateBase):
    section_kind: Literal["checklist"] = "checklist"
    items: list[ChecklistItem] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_items(self) -> "ChecklistSectionTemplate":
        if not self.items:
            raise ValueError(
                "checklist sections must define at least one item")
        return self


class FieldSectionTemplate(SectionTemplateBase):
    section_kind: Literal["fields"] = "fields"
    fields: list[FieldTemplate] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_fields(self) -> "FieldSectionTemplate":
        if not self.fields:
            raise ValueError("field sections must define at least one field")
        return self


class LinkSectionTemplate(SectionTemplateBase):
    section_kind: Literal["links"] = "links"
    links: list[DocumentLink] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_links(self) -> "LinkSectionTemplate":
        if not self.links:
            raise ValueError("link sections must define at least one target")
        return self


class TreeSectionTemplate(SectionTemplateBase):
    section_kind: Literal["tree"] = "tree"
    tree_kind: TreeKind
    signatures_allowed: bool = False
    must_be_first: bool = False
    reuse_parent_tree: bool = False


SectionTemplate: TypeAlias = Annotated[
    ProseSectionTemplate
    | ChecklistSectionTemplate
    | FieldSectionTemplate
    | LinkSectionTemplate
    | TreeSectionTemplate,
    Field(discriminator="section_kind"),
]


class FrontmatterBase(SchemaModel):
    scope: RuleScope = "shared"
    audience: Audience = "agent"
    purpose: str
    applies_when: list[str] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)
    read_directly: bool = True
    tightens_paths: list[str] = Field(default_factory=list)

    @field_validator("purpose")
    @classmethod
    def validate_purpose(cls, value: str) -> str:
        return _clean_text(value)

    @field_validator("applies_when", "tags")
    @classmethod
    def validate_string_lists(cls, values: list[str]) -> list[str]:
        return _clean_text_list(values)

    @field_validator("tightens_paths")
    @classmethod
    def validate_tightens_paths(cls, values: list[str]) -> list[str]:
        return [_normalize_path(value) for value in values if value.strip()]

    @model_validator(mode="after")
    def validate_scope_contract(self) -> "FrontmatterBase":
        if self.scope == "project" and not self.tightens_paths:
            raise ValueError(
                "project-scoped documents must declare tightens_paths")
        if self.scope == "shared" and self.tightens_paths:
            raise ValueError(
                "shared documents must not declare tightens_paths")
        return self


class NavigationalFrontmatter(FrontmatterBase):
    doc_class: Literal["navigational"] = "navigational"
    rule_kind: Literal["navigation"] = "navigation"
    entrypoint: bool = True
    read_strategy: Literal["progressive"] = "progressive"
    child_paths: list[str] = Field(default_factory=list)

    @field_validator("child_paths")
    @classmethod
    def validate_child_paths(cls, values: list[str]) -> list[str]:
        return [_normalize_path(value) for value in values if value.strip()]


class PolicyFrontmatter(FrontmatterBase):
    doc_class: Literal["policy"] = "policy"
    rule_kind: Literal["policy"] = "policy"
    read_directly: bool = False
    escalation_paths: list[str] = Field(default_factory=list)

    @field_validator("escalation_paths")
    @classmethod
    def validate_escalation_paths(cls, values: list[str]) -> list[str]:
        return [_normalize_path(value) for value in values if value.strip()]


class ExecutionFrontmatter(FrontmatterBase):
    doc_class: Literal["execution"] = "execution"
    rule_kind: Literal["execution"] = "execution"
    stage: ExecutionStage
    same_artifact_family: str = "execution"
    read_directly: bool = False
    escalation_paths: list[str] = Field(default_factory=list)

    @field_validator("same_artifact_family")
    @classmethod
    def validate_family(cls, value: str) -> str:
        return _clean_text(value)

    @field_validator("escalation_paths")
    @classmethod
    def validate_escalation_paths(cls, values: list[str]) -> list[str]:
        return [_normalize_path(value) for value in values if value.strip()]


class RuleDocumentTemplateBase(SchemaModel):
    key: str
    title: str
    path: str
    sections: list[SectionTemplate] = Field(default_factory=list)
    review_checks: list[ChecklistItem] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)

    @field_validator("key", "title")
    @classmethod
    def validate_text(cls, value: str) -> str:
        return _clean_text(value)

    @field_validator("path")
    @classmethod
    def validate_path(cls, value: str) -> str:
        return _normalize_path(value)

    @field_validator("notes")
    @classmethod
    def validate_notes(cls, values: list[str]) -> list[str]:
        return _clean_text_list(values)

    @model_validator(mode="after")
    def validate_sections(self) -> "RuleDocumentTemplateBase":
        if not self.sections:
            raise ValueError("documents must define at least one section")

        section_keys: list[str] = []
        section_headings: list[str] = []
        first_section_required = False

        for index, section in enumerate(self.sections):
            if section.key in section_keys:
                raise ValueError(f"duplicate section key: {section.key}")
            if section.heading in section_headings:
                raise ValueError(
                    f"duplicate section heading: {section.heading}")
            section_keys.append(section.key)
            section_headings.append(section.heading)
            if isinstance(section, TreeSectionTemplate) and section.must_be_first:
                if index != 0:
                    raise ValueError(
                        f"tree section '{section.heading}' must be the first section"
                    )
                first_section_required = True

        if sum(
                1
                for section in self.sections
                if isinstance(section, TreeSectionTemplate) and section.must_be_first
        ) > 1:
            raise ValueError(
                "only one tree section can require first position")

        if first_section_required and not isinstance(self.sections[0], TreeSectionTemplate):
            raise ValueError(
                "the first section must be the required tree section")

        review_keys = [item.key for item in self.review_checks]
        if len(review_keys) != len(set(review_keys)):
            raise ValueError("duplicate review check keys are not allowed")

        return self


class NavigationalRuleTemplate(RuleDocumentTemplateBase):
    doc_kind: Literal["navigational"] = "navigational"
    frontmatter: NavigationalFrontmatter

    @model_validator(mode="after")
    def validate_navigation(self) -> "NavigationalRuleTemplate":
        if self.path != "INDEX.md" and not self.path.endswith("/INDEX.md"):
            raise ValueError("navigational documents must use INDEX.md paths")
        if not any(isinstance(section, LinkSectionTemplate) for section in self.sections):
            raise ValueError(
                "navigational documents must include at least one link section")

        link_paths = {
            link.path
            for section in self.sections
            if isinstance(section, LinkSectionTemplate)
            for link in section.links
        }
        missing_child_paths = set(self.frontmatter.child_paths) - link_paths
        if missing_child_paths:
            missing = ", ".join(sorted(missing_child_paths))
            raise ValueError(
                f"child_paths must be represented in link sections: {missing}"
            )
        return self


class PolicyRuleTemplate(RuleDocumentTemplateBase):
    doc_kind: Literal["policy"] = "policy"
    frontmatter: PolicyFrontmatter


class ExecutionRuleTemplate(RuleDocumentTemplateBase):
    doc_kind: Literal["execution"] = "execution"
    frontmatter: ExecutionFrontmatter
    handoff_checks: list[ChecklistItem] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_execution(self) -> "ExecutionRuleTemplate":
        tree_sections = [
            section for section in self.sections if isinstance(section, TreeSectionTemplate)
        ]
        if len(tree_sections) != 1:
            raise ValueError(
                "execution documents must define exactly one tree section")

        tree = tree_sections[0]
        if self.frontmatter.stage == "big_picture":
            if tree.tree_kind != "file":
                raise ValueError(
                    "big-picture execution documents require a file tree")
            if tree.signatures_allowed:
                raise ValueError(
                    "big-picture execution documents must not allow signatures in the tree"
                )
        if self.frontmatter.stage == "step":
            if tree.tree_kind != "implementation":
                raise ValueError(
                    "step execution documents require an implementation tree")
            if not tree.signatures_allowed:
                raise ValueError(
                    "step execution documents must allow signatures in the tree"
                )

        handoff_keys = [item.key for item in self.handoff_checks]
        if len(handoff_keys) != len(set(handoff_keys)):
            raise ValueError("duplicate handoff check keys are not allowed")
        return self


RuleDocumentTemplate: TypeAlias = Annotated[
    NavigationalRuleTemplate | PolicyRuleTemplate | ExecutionRuleTemplate,
    Field(discriminator="doc_kind"),
]


class RuleTreeTemplate(SchemaModel):
    root_path: str = "rules"
    documents: list[RuleDocumentTemplate] = Field(default_factory=list)

    @field_validator("root_path")
    @classmethod
    def validate_root_path(cls, value: str) -> str:
        return _normalize_path(value)

    @model_validator(mode="after")
    def validate_documents(self) -> "RuleTreeTemplate":
        document_keys = [document.key for document in self.documents]
        if len(document_keys) != len(set(document_keys)):
            raise ValueError(
                "document keys must be unique across the rule tree")

        document_paths = [document.path for document in self.documents]
        if len(document_paths) != len(set(document_paths)):
            raise ValueError(
                "document paths must be unique across the rule tree")

        return self


__all__ = [
    "Audience",
    "ChecklistItem",
    "ChecklistSectionTemplate",
    "DocumentClass",
    "DocumentLink",
    "ExecutionFrontmatter",
    "ExecutionRuleTemplate",
    "ExecutionStage",
    "FieldSectionTemplate",
    "FieldTemplate",
    "FieldValueKind",
    "FrontmatterBase",
    "LinkSectionTemplate",
    "NavigationalFrontmatter",
    "NavigationalRuleTemplate",
    "PolicyFrontmatter",
    "PolicyRuleTemplate",
    "ProseSectionTemplate",
    "ReadStrategy",
    "RuleScope",
    "RuleDocumentTemplate",
    "RuleDocumentTemplateBase",
    "RuleKind",
    "RuleTreeTemplate",
    "SchemaModel",
    "SectionTemplate",
    "SectionTemplateBase",
    "TreeKind",
    "TreeSectionTemplate",
]
