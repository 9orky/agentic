from __future__ import annotations

import unittest
from pathlib import Path
from unittest.mock import patch

from click.testing import CliRunner

from agentic.cli import agentic_cli
from agentic.features.workspace_contract.rules.application.queries import build_rule_schema_report
from agentic.features.workspace_contract.rules.domain import RuleDocumentFile, RuleDocumentRepository


class _FakeRuleDocumentRepository(RuleDocumentRepository):
    def __init__(self, documents: tuple[RuleDocumentFile, ...]) -> None:
        self._documents = documents

    def find(self) -> tuple[RuleDocumentFile, ...]:
        return self._documents


class RuleSchemaCliTests(unittest.TestCase):
    def setUp(self) -> None:
        self.runner = CliRunner()

    def test_build_rule_schema_report_marks_collection_complete_for_valid_packaged_rules(self) -> None:
        report = build_rule_schema_report(
            repository=_FakeRuleDocumentRepository(_valid_rule_documents()),
        )

        self.assertEqual(report.documents_discovered, 4)
        self.assertEqual(report.documents_checked, 4)
        self.assertTrue(report.collection_complete)
        self.assertFalse(report.has_findings)

    def test_build_rule_schema_report_reports_missing_metadata_reference(self) -> None:
        report = build_rule_schema_report(
            repository=_FakeRuleDocumentRepository(
                _rule_documents_with_missing_reference()),
        )

        self.assertTrue(report.has_findings)
        self.assertEqual(report.documents_with_issues, 1)
        target_report = next(
            document for document in report.documents if document.path == Path("shared/change/REFACTORING.md")
        )
        self.assertEqual(len(target_report.violations), 1)
        self.assertEqual(
            target_report.violations[0].code, "missing-reference-target")
        self.assertEqual(
            target_report.violations[0].reference_path, "../verification/DOES_NOT_EXIST.md")

    def test_check_rule_schema_command_renders_collection_coverage(self) -> None:
        repository = _FakeRuleDocumentRepository(_valid_rule_documents())

        with patch(
            "agentic.features.workspace_contract.rules.ui.cli.build_rule_schema_report",
            side_effect=lambda: build_rule_schema_report(
                repository=repository),
        ):
            result = self.runner.invoke(
                agentic_cli, ["check-rule-schema"], catch_exceptions=False)

        self.assertEqual(result.exit_code, 0, result.output)
        self.assertIn("Documents discovered: 4.", result.output)
        self.assertIn("Documents checked: 4.", result.output)
        self.assertIn("Collection coverage: complete.", result.output)


def _valid_rule_documents() -> tuple[RuleDocumentFile, ...]:
    return (
        RuleDocumentFile(
            path=Path("INDEX.md"),
            content="""---
doc_class: navigational
rule_kind: navigation
audience: agent
purpose: Route packaged rules.
applies_when:
  - Starting packaged rule selection.
tags:
  - rules
entrypoint: true
read_strategy: progressive
read_directly: true
child_paths:
  - shared/INDEX.md
---

# Rules

## Stop Or Descend

- Read [shared/INDEX.md](shared/INDEX.md).

## Branches

- [shared/INDEX.md](shared/INDEX.md): packaged shared guidance

## Review Checks

- The next read is explicit.
""",
        ),
        RuleDocumentFile(
            path=Path("shared/INDEX.md"),
            content="""---
doc_class: navigational
rule_kind: navigation
audience: agent
purpose: Route packaged shared rules.
applies_when:
  - Shared guidance is needed.
tags:
  - shared
entrypoint: true
read_strategy: progressive
read_directly: true
child_paths:
  - change/INDEX.md
---

# Shared Rules

## Use This Branch When

- Shared packaged guidance is needed.

## Stop Or Descend

- Read [change/INDEX.md](change/INDEX.md).

## Branches

- [change/INDEX.md](change/INDEX.md): packaged change guidance

## Review Checks

- The next read is explicit.
""",
        ),
        RuleDocumentFile(
            path=Path("shared/change/INDEX.md"),
            content="""---
doc_class: navigational
rule_kind: navigation
audience: agent
purpose: Route change guidance.
applies_when:
  - Change guidance is needed.
tags:
  - change
entrypoint: true
read_strategy: progressive
read_directly: true
child_paths:
  - REFACTORING.md
---

# Change

## Use This Branch When

- Change guidance is needed.

## Stop Or Descend

- Read [REFACTORING.md](REFACTORING.md).

## Branches

- [REFACTORING.md](REFACTORING.md): refactoring guidance

## Review Checks

- The next read is explicit.
""",
        ),
        RuleDocumentFile(
            path=Path("shared/change/REFACTORING.md"),
            content="""---
doc_class: policy
rule_kind: policy
audience: agent
purpose: Govern refactoring decisions.
applies_when:
  - Existing code is being reshaped.
tags:
  - change
read_directly: false
scope: shared
tightens_paths: []
escalation_paths:
  - ../INDEX.md
---

# Refactoring

## Required Decisions

- State the target design.

## Core Rules

- Start from the target design.

## Review Checks

- The target design is explicit.
""",
        ),
    )


def _rule_documents_with_missing_reference() -> tuple[RuleDocumentFile, ...]:
    documents = list(_valid_rule_documents())
    documents[-1] = RuleDocumentFile(
        path=Path("shared/change/REFACTORING.md"),
        content="""---
doc_class: policy
rule_kind: policy
audience: agent
purpose: Govern refactoring decisions.
applies_when:
  - Existing code is being reshaped.
tags:
  - change
read_directly: false
scope: shared
tightens_paths: []
escalation_paths:
  - ../verification/DOES_NOT_EXIST.md
---

# Refactoring

## Required Decisions

- State the target design.

## Core Rules

- Start from the target design.

## Review Checks

- The target design is explicit.
""",
    )
    return tuple(documents)


if __name__ == "__main__":
    unittest.main()
