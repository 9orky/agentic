from __future__ import annotations

import sys
from dataclasses import dataclass

from ..domain import CheckerError


@dataclass(frozen=True)
class ExtractorSpec:
    command: str
    resource_name: str


class ExtractorSpecRegistry:
    def __init__(self) -> None:
        self._extractor_specs: dict[str, ExtractorSpec] = {
            "python": ExtractorSpec(
                command=sys.executable,
                resource_name="python_extractor.py",
            ),
            "typescript": ExtractorSpec(
                command="node",
                resource_name="typescript_extractor.js",
            ),
            "php": ExtractorSpec(
                command="php",
                resource_name="php_extractor.php",
            ),
        }

    def get(self, language: str) -> ExtractorSpec:
        runtime = self._extractor_specs.get(language)
        if runtime is None:
            raise CheckerError(f"Unsupported language '{language}'")
        return runtime


__all__ = ["ExtractorSpec", "ExtractorSpecRegistry"]
