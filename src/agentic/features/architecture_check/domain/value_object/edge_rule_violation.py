from dataclasses import dataclass


@dataclass(frozen=True)
class EdgeRuleViolation:
    source_id: str
    target_id: str
    source_pattern: str
    target_pattern: str
    rule_name: str
