from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from ...domain import RuleDocumentClass


@dataclass(frozen=True)
class RuleMarkdownDocument:
    source_path: Path
    headings: tuple[str, ...]
    section_headings: tuple[str, ...]
    anchor_headings: tuple[str, ...]
    navigation_targets: tuple[str, ...]
    declared_document_class: RuleDocumentClass | None = None

    @property
    def document_class(self) -> RuleDocumentClass:
        if self.declared_document_class is not None:
            return self.declared_document_class
        if any(heading.endswith("Options") for heading in self.headings):
            return RuleDocumentClass.NAVIGATIONAL
        if "Navigation Rule" in self.headings:
            return RuleDocumentClass.NAVIGATIONAL
        return RuleDocumentClass.LEAF

    @property
    def has_navigation_targets(self) -> bool:
        return bool(self.navigation_targets)
