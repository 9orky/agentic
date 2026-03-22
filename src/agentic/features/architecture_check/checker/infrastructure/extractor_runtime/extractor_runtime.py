from __future__ import annotations

from pathlib import Path
from typing import Protocol

from ...domain.value_object import ExtractionResult
from ..extractor_registry import ExtractorSpec


class ExtractorRuntime(Protocol):
    def run(self, spec: ExtractorSpec, project_root: Path, exclusions: list[str]) -> ExtractionResult:
        ...
