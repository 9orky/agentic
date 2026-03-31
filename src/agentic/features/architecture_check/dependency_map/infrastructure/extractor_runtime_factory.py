from __future__ import annotations

from .extractor_runtime import ExtractorRuntime, SubprocessExtractorRuntime


class ExtractorRuntimeFactory:
    def create(self) -> ExtractorRuntime:
        return SubprocessExtractorRuntime()


__all__ = ["ExtractorRuntimeFactory"]
