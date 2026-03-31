from dataclasses import dataclass


@dataclass(frozen=True)
class FlowAnalyzerConfig:
    layers: tuple[str, ...]
    module_tag: str
