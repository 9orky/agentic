from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from .rules import (
    RuleDocumentReport,
    RuleSchemaReport,
    RuleSchemaViolationReport,
    build_rule_schema_report,
)
from .workspace_sync.application import build_default_bootstrap_project, build_default_describe_workspace_contract, build_default_update_project
from .workspace_sync.domain import WorkspaceContractSummary


class BootstrapError(RuntimeError):
    """Raised when workspace-contract boundary operations fail."""


@dataclass
class SyncResult:
    target_dir: Path
    created_dir: bool = False
    created_files: list[Path] = field(default_factory=list)
    updated_files: list[Path] = field(default_factory=list)
    preserved_files: list[Path] = field(default_factory=list)


__all__ = [
    "BootstrapError",
    "RuleDocumentReport",
    "RuleSchemaReport",
    "RuleSchemaViolationReport",
    "SyncResult",
    "WorkspaceContractSummary",
    "bootstrap_project",
    "build_rule_schema_report",
    "describe_workspace_contract",
    "update_project",
]


def bootstrap_project(project_root: Path) -> SyncResult:
    return _coerce_sync_result(_run_sync_command(build_default_bootstrap_project(), project_root))


def update_project(project_root: Path) -> SyncResult:
    return _coerce_sync_result(_run_sync_command(build_default_update_project(), project_root))


def describe_workspace_contract(project_root: Path) -> WorkspaceContractSummary:
    try:
        return build_default_describe_workspace_contract().execute(project_root)
    except NotADirectoryError as exc:
        raise BootstrapError(str(exc)) from exc


def _run_sync_command(command, project_root: Path) -> dict[str, object]:
    try:
        return command.execute(project_root)
    except NotADirectoryError as exc:
        raise BootstrapError(str(exc)) from exc


def _coerce_sync_result(result: dict[str, object]) -> SyncResult:
    return SyncResult(
        target_dir=result["target_dir"],
        created_dir=bool(result["created_dir"]),
        created_files=list(result["created_files"]),
        updated_files=list(result["updated_files"]),
        preserved_files=list(result["preserved_files"]),
    )
