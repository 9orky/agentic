from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from ...domain import RuleDocumentClass


@dataclass(frozen=True)
class RuleSchemaDriftFinding:
    scope: str
    document_path: Path
    document_class: RuleDocumentClass
    code: str
    message: str
    section_heading: str | None = None
