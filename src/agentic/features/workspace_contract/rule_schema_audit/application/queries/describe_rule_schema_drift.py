from __future__ import annotations

from pathlib import Path

from ..services.rule_schema_validation import (
    RuleSchemaValidationResult,
    RuleSchemaValidationService,
    build_default_rule_schema_validation_service,
)


class DescribeRuleSchemaDrift:
    def __init__(
        self,
        *,
        validation_service: RuleSchemaValidationService,
    ) -> None:
        self._validation_service = validation_service

    def execute(
        self,
        project_root: Path,
        *,
        include_local_mirror: bool = True,
    ) -> RuleSchemaValidationResult:
        return self._validation_service.describe(
            project_root,
            include_local_mirror=include_local_mirror,
        )


def build_default_describe_rule_schema_drift() -> DescribeRuleSchemaDrift:
    return DescribeRuleSchemaDrift(
        validation_service=build_default_rule_schema_validation_service(),
    )
