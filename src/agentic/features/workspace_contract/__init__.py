from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from .contract.application import build_default_bootstrap_project
from .contract.application import build_default_describe_rule_schema_drift
from .contract.application import build_default_describe_workspace_contract
from .contract.application import build_default_update_project
from .contract.application import RuleSchemaValidationResult
from .contract.domain import WorkspaceContractSummary


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
    "RuleSchemaValidationResult",
    "SyncResult",
    "WorkspaceContractSummary",
    "bootstrap_project",
    "describe_rule_schema_drift",
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


def describe_rule_schema_drift(
    project_root: Path,
    *,
    include_local_mirror: bool = True,
) -> RuleSchemaValidationResult:
    try:
        return build_default_describe_rule_schema_drift().execute(
            project_root,
            include_local_mirror=include_local_mirror,
        )
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
