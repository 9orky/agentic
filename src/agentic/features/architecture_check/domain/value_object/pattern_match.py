from dataclasses import dataclass


@dataclass(frozen=True)
class PatternMatch:
    captures: tuple[str, ...]
