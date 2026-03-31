from __future__ import annotations

import re
from pathlib import Path

from ...domain import RuleDocumentClass
from .rule_markdown_document import RuleMarkdownDocument


class RuleMarkdownParser:
    _heading_pattern = re.compile(
        r"^(?P<marker>##+)\s+(?P<heading>.+?)\s*$", re.MULTILINE)
    _link_pattern = re.compile(r"\[[^\]]+\]\((?P<target>[^)#]+\.md)\)")
    _frontmatter_class_pattern = re.compile(
        r"\A---\s*\n(?P<frontmatter>.*?)\n---\s*\n",
        re.DOTALL,
    )
    _declared_class_pattern = re.compile(
        r"^document_class\s*:\s*(?P<value>.+?)\s*$", re.MULTILINE)
    _inline_class_pattern = re.compile(
        r"^Document Class\s*:\s*(?P<value>.+?)\s*$", re.MULTILINE)

    def parse(self, document_text: str, source_path: Path) -> RuleMarkdownDocument:
        declared_document_class = self._parse_declared_document_class(
            document_text)
        headings: list[str] = []
        section_headings: list[str] = []
        anchor_headings: list[str] = []
        for match in self._heading_pattern.finditer(document_text):
            heading = match.group("heading")
            headings.append(heading)
            heading_level = len(match.group("marker"))
            if heading_level == 2:
                section_headings.append(heading)
            elif heading_level == 3:
                anchor_headings.append(heading)
        navigation_targets = tuple(
            match.group("target")
            for match in self._link_pattern.finditer(document_text)
        )

        return RuleMarkdownDocument(
            source_path=source_path,
            headings=tuple(headings),
            section_headings=tuple(section_headings),
            anchor_headings=tuple(anchor_headings),
            navigation_targets=navigation_targets,
            declared_document_class=declared_document_class,
        )

    def _parse_declared_document_class(self, document_text: str) -> RuleDocumentClass | None:
        frontmatter_match = self._frontmatter_class_pattern.match(
            document_text)
        if frontmatter_match is not None:
            frontmatter_text = frontmatter_match.group("frontmatter")
            class_match = self._declared_class_pattern.search(frontmatter_text)
            if class_match is not None:
                return RuleDocumentClass.from_literal(class_match.group("value"))

        inline_match = self._inline_class_pattern.search(document_text)
        if inline_match is None:
            return None
        return RuleDocumentClass.from_literal(inline_match.group("value"))
