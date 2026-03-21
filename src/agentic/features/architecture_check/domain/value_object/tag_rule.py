from dataclasses import dataclass


@dataclass(frozen=True)
class TagRule:
    name: str
    match: str
