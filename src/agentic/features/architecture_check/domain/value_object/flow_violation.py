from dataclasses import dataclass


@dataclass(frozen=True)
class FlowViolation:
    violation_type: str
    path: tuple[str, ...]
    violation_index: int
    rule_name: str
    message: str
