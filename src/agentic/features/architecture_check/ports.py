from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

from .domain.extractor_contract import ExtractionResult


@dataclass(frozen=True)
class ExtractorSpec:
    command: str
    resource_name: str


class ExtractorRuntime(Protocol):
    def run(self, spec: ExtractorSpec, project_root: Path, exclusions: list[str]) -> ExtractionResult:
        ...
