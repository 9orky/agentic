from __future__ import annotations

from ...infrastructure import ExtractorRuntime, SubprocessExtractorRuntime


class ExtractorRuntimeFactory:
    def create(self) -> ExtractorRuntime:
        return SubprocessExtractorRuntime()


default_extractor_runtime = ExtractorRuntimeFactory().create

__all__ = ["ExtractorRuntimeFactory", "default_extractor_runtime"]
