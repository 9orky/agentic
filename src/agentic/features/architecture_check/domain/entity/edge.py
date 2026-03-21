from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Edge:
    from_id: str
    to_id: str
    kind: str = "import"
