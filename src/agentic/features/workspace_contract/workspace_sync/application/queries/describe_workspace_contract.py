from __future__ import annotations

from pathlib import Path

from ...domain import WorkspaceContractSummary
from ..services.workspace_contract_summary_service import (
    WorkspaceContractSummaryService,
    build_default_workspace_contract_summary_service,
)


class DescribeWorkspaceContract:
    def __init__(
        self,
        *,
        summary_service: WorkspaceContractSummaryService,
    ) -> None:
        self._summary_service = summary_service

    def execute(self, project_root: Path) -> WorkspaceContractSummary:
        return self._summary_service.describe(project_root)


def build_default_describe_workspace_contract() -> DescribeWorkspaceContract:
    return DescribeWorkspaceContract(
        summary_service=build_default_workspace_contract_summary_service(),
    )
