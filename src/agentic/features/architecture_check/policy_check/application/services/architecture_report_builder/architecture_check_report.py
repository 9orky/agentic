from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from ....domain import EdgeRuleViolation, FlowViolation


@dataclass(frozen=True)
class ArchitectureCheckReport:
    project_root: Path
    config_path: Path
    config_format: str
    language: str
    runtime_command: str
    files_found: int = 0
    files_excluded: int = 0
    files_checked: int = 0
    violations: tuple[EdgeRuleViolation | FlowViolation, ...] = ()
    check_error: str | None = None

    def to_json_dict(self) -> dict[str, Any]:
        return {
            "project_root": str(self.project_root),
            "config_path": str(self.config_path),
            "config_format": self.config_format,
            "language": self.language,
            "runtime_command": self.runtime_command,
            "files_found": self.files_found,
            "files_excluded": self.files_excluded,
            "files_checked": self.files_checked,
            "check_error": self.check_error,
            "violations": [self._serialize_violation(violation) for violation in self.violations],
        }

    def _serialize_violation(self, violation: EdgeRuleViolation | FlowViolation) -> dict[str, Any]:
        payload = asdict(violation)
        if isinstance(violation, EdgeRuleViolation):
            payload["type"] = "edge-rule"
            payload["path"] = [violation.source_id, violation.target_id]
            payload["violation_index"] = 1
            return payload

        payload["type"] = violation.violation_type
        payload["path"] = list(violation.path)
        return payload
