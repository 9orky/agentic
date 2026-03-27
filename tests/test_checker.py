import json
import os
import agentic.features.architecture_check.checker.domain as architecture_check_domain
import agentic.features.architecture_check.checker.domain.entity as architecture_check_domain_entity
import agentic.features.architecture_check.checker.domain.service as architecture_check_domain_service
import agentic.features.architecture_check.checker.domain.value_object as architecture_check_domain_value_object
from pathlib import Path
import shutil
from tempfile import TemporaryDirectory
from unittest.mock import Mock, patch
import unittest

from agentic.features.architecture_check import CheckerError, run_architecture_check


class ArchitectureCheckDomainPackageTests(unittest.TestCase):
    def test_domain_package_exports_expected_public_seam(self) -> None:
        self.assertEqual(
            architecture_check_domain.__all__,
            [
                "ArchitectureCheckConfig",
                "ArchitectureCheckConfigError",
                "ArchitecturePolicyEvaluator",
                "BackwardFlowAnalyzer",
                "BoundaryRule",
                "CheckerError",
                "ConfigLoadResult",
                "ConfigTagRule",
                "CycleDetector",
                "DependencyGraph",
                "DependencyRule",
                "Edge",
                "EdgeRuleViolation",
                "ExtractedFile",
                "ExtractionResult",
                "ExtractionSummary",
                "ExtractorContractError",
                "FlowAnalyzerConfig",
                "FlowRuleSet",
                "FlowViolation",
                "NoCyclesAnalyzer",
                "NoReentryAnalyzer",
                "Node",
                "NodeSelector",
                "PatternMatch",
                "RuleSet",
                "TagRule",
            ],
        )

    def test_domain_entity_anchor_exports_expected_public_seam(self) -> None:
        self.assertEqual(
            architecture_check_domain_entity.__all__,
            ["DependencyGraph", "Edge", "Node"],
        )

    def test_domain_service_anchor_exports_expected_public_seam(self) -> None:
        self.assertEqual(
            architecture_check_domain_service.__all__,
            [
                "ArchitecturePolicyEvaluator",
                "BackwardFlowAnalyzer",
                "CycleDetector",
                "NoCyclesAnalyzer",
                "NoReentryAnalyzer",
            ],
        )

    def test_domain_value_object_anchor_exports_expected_public_seam(self) -> None:
        self.assertEqual(
            architecture_check_domain_value_object.__all__,
            [
                "ArchitectureCheckConfig",
                "ArchitectureCheckConfigError",
                "BoundaryRule",
                "CheckerError",
                "ConfigLoadResult",
                "ConfigTagRule",
                "DependencyRule",
                "EdgeRuleViolation",
                "ExtractedFile",
                "ExtractionResult",
                "ExtractionSummary",
                "ExtractorContractError",
                "FlowAnalyzerConfig",
                "FlowRuleSet",
                "FlowViolation",
                "NodeSelector",
                "PatternMatch",
                "RuleSet",
                "TagRule",
            ],
        )

    def test_domain_directory_matches_allowed_anchor_shape(self) -> None:
        domain_dir = Path(architecture_check_domain.__file__).resolve().parent
        entries = {
            path.name
            for path in domain_dir.iterdir()
            if path.name != "__pycache__"
        }

        self.assertEqual(
            entries, {"__init__.py", "entity", "service", "value_object"})


class CheckerTests(unittest.TestCase):
    @patch("agentic.features.architecture_check.checker.infrastructure.extractor_runtime.subprocess.run")
    def test_rejects_non_json_extractor_output_through_public_seam(self, mock_run: Mock) -> None:
        with TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            (project_root / "agentic").mkdir()
            (project_root / "agentic" / "agentic.yaml").write_text(
                "language: python\nrules:\n  boundaries: []\n",
                encoding="utf-8",
            )
            mock_run.return_value = Mock(
                stdout="not-json", stderr="", returncode=0)

            with self.assertRaises(CheckerError) as context:
                run_architecture_check(project_root)

            self.assertIn("valid JSON", str(context.exception))

    @patch("agentic.features.architecture_check.checker.infrastructure.extractor_runtime.subprocess.run")
    def test_rejects_invalid_extractor_contract_through_public_seam(self, mock_run: Mock) -> None:
        with TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            (project_root / "agentic").mkdir()
            (project_root / "agentic" / "agentic.yaml").write_text(
                "language: python\nrules:\n  boundaries: []\n",
                encoding="utf-8",
            )
            mock_run.return_value = Mock(
                stdout=json.dumps(
                    {"src/domain/logic.py": {"imports": ["src.infra.database"], "classes": []}}),
                stderr="",
                returncode=0,
            )

            with self.assertRaises(CheckerError) as context:
                run_architecture_check(project_root)

            self.assertIn("src/domain/logic.py", str(context.exception))

    def test_detects_python_boundary_violation(self) -> None:
        with TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            (project_root / "src" / "domain").mkdir(parents=True)
            (project_root / "src" / "infra").mkdir(parents=True)
            (project_root / "agentic").mkdir()

            (project_root / "src" / "infra" / "database.py").write_text(
                "class Database:\n    pass\n",
                encoding="utf-8",
            )
            (project_root / "src" / "domain" / "logic.py").write_text(
                "from src.infra.database import Database\n",
                encoding="utf-8",
            )
            (project_root / "agentic" / "agentic.yaml").write_text(
                "language: python\n"
                "exclusions:\n"
                "  - agentic/\n"
                "rules:\n"
                "  boundaries:\n"
                "    - source: src/domain\n"
                "      disallow:\n"
                "        - src/infra\n",
                encoding="utf-8",
            )

            result = run_architecture_check(project_root)

            self.assertEqual(result.files_found, 2)
            self.assertEqual(result.files_excluded, 0)
            self.assertEqual(result.files_checked, 2)
            self.assertEqual(len(result.violations), 1)
            self.assertIn("src/domain/logic.py", result.violations[0])
            self.assertIn("src/infra", result.violations[0])

    def test_detects_src_layout_package_import_violation(self) -> None:
        with TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            (project_root / "src" / "agentic" / "domain").mkdir(parents=True)
            (project_root / "src" / "agentic" / "infra").mkdir(parents=True)
            (project_root / "agentic").mkdir()

            (project_root / "src" / "agentic" / "domain" /
             "__init__.py").write_text("", encoding="utf-8")
            (project_root / "src" / "agentic" / "infra" /
             "__init__.py").write_text("", encoding="utf-8")
            (project_root / "src" / "agentic" / "infra" / "database.py").write_text(
                "class Database:\n    pass\n",
                encoding="utf-8",
            )
            (project_root / "src" / "agentic" / "domain" / "logic.py").write_text(
                "from agentic.infra.database import Database\n",
                encoding="utf-8",
            )
            (project_root / "agentic" / "agentic.yaml").write_text(
                "language: python\n"
                "exclusions:\n"
                "  - agentic/\n"
                "rules:\n"
                "  boundaries:\n"
                "    - source: src/agentic/domain\n"
                "      disallow:\n"
                "        - src/agentic/infra\n",
                encoding="utf-8",
            )

            result = run_architecture_check(project_root)

            self.assertEqual(len(result.violations), 1)
            self.assertIn("src/agentic/domain/logic.py", result.violations[0])
            self.assertIn("src/agentic/infra/database.py",
                          result.violations[0])

    def test_detects_relative_import_violation(self) -> None:
        with TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            (project_root / "src" / "app" / "ui").mkdir(parents=True)
            (project_root / "src" / "app" / "infra").mkdir(parents=True)
            (project_root / "agentic").mkdir()

            (project_root / "src" / "app" / "ui" /
             "__init__.py").write_text("", encoding="utf-8")
            (project_root / "src" / "app" / "infra" /
             "__init__.py").write_text("", encoding="utf-8")
            (project_root / "src" / "app" / "infra" / "db.py").write_text(
                "class Db:\n    pass\n",
                encoding="utf-8",
            )
            (project_root / "src" / "app" / "ui" / "view.py").write_text(
                "from ..infra.db import Db\n",
                encoding="utf-8",
            )
            (project_root / "agentic" / "agentic.yaml").write_text(
                "language: python\n"
                "exclusions:\n"
                "  - agentic/\n"
                "rules:\n"
                "  boundaries:\n"
                "    - source: src/app/ui\n"
                "      disallow:\n"
                "        - src/app/infra\n",
                encoding="utf-8",
            )

            result = run_architecture_check(project_root)

            self.assertEqual(len(result.violations), 1)
            self.assertIn("src/app/ui/view.py", result.violations[0])
            self.assertIn("src/app/infra/db.py", result.violations[0])

    def test_glob_rule_blocks_cross_feature_internal_imports(self) -> None:
        with TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            (project_root / "src" / "features" / "orders").mkdir(parents=True)
            (project_root / "src" / "features" /
             "billing" / "internal").mkdir(parents=True)
            (project_root / "agentic").mkdir()

            (project_root / "src" / "features" / "orders" / "service.py").write_text(
                "from src.features.billing.internal.db import DbClient\n",
                encoding="utf-8",
            )
            (project_root / "agentic" / "agentic.yaml").write_text(
                "language: python\n"
                "rules:\n"
                "  boundaries:\n"
                "    - source: src/features/*\n"
                "      disallow:\n"
                "        - src/features/*\n"
                "      allow_same_match: true\n"
                "      allow:\n"
                "        - src/features/*\n",
                encoding="utf-8",
            )

            result = run_architecture_check(project_root)

            self.assertEqual(len(result.violations), 1)
            self.assertIn("src/features/billing/internal/db",
                          result.violations[0])

    def test_glob_rule_allows_same_feature_imports(self) -> None:
        with TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            (project_root / "src" / "features" / "orders").mkdir(parents=True)
            (project_root / "agentic").mkdir()

            (project_root / "src" / "features" / "orders" / "service.py").write_text(
                "from src.features.orders.model import Order\n",
                encoding="utf-8",
            )
            (project_root / "agentic" / "agentic.yaml").write_text(
                "language: python\n"
                "rules:\n"
                "  boundaries:\n"
                "    - source: src/features/*\n"
                "      disallow:\n"
                "        - src/features/*\n"
                "      allow_same_match: true\n",
                encoding="utf-8",
            )

            result = run_architecture_check(project_root)

            self.assertEqual(result.violations, [])

    def test_result_reports_excluded_and_checked_files(self) -> None:
        with TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            (project_root / "src" / "domain").mkdir(parents=True)
            (project_root / "src" / "generated").mkdir(parents=True)
            (project_root / "agentic").mkdir()

            (project_root / "src" / "domain" / "logic.py").write_text(
                "from src.domain.helpers import helper\n",
                encoding="utf-8",
            )
            (project_root / "src" / "generated" / "client.py").write_text(
                "from src.domain.logic import Logic\n",
                encoding="utf-8",
            )
            (project_root / "agentic" / "agentic.yaml").write_text(
                "language: python\n"
                "exclusions:\n"
                "  - src/generated\n"
                "rules:\n"
                "  boundaries:\n"
                "    - source: src/domain\n"
                "      disallow:\n"
                "        - src/infra\n",
                encoding="utf-8",
            )

            result = run_architecture_check(project_root)

            self.assertEqual(result.files_found, 2)
            self.assertEqual(result.files_excluded, 1)
            self.assertEqual(result.files_checked, 1)
            self.assertEqual(result.violations, [])

    def test_hardcoded_literals_and_defaults_do_not_create_false_positive_violations(self) -> None:
        with TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            (project_root / "src" / "domain").mkdir(parents=True)
            (project_root / "src" / "infra").mkdir(parents=True)
            (project_root / "agentic").mkdir()

            (project_root / "src" / "domain" / "helpers.py").write_text(
                "DEFAULT_REGION = 'eu-west-1'\n",
                encoding="utf-8",
            )
            (project_root / "src" / "infra" / "database.py").write_text(
                "class Database:\n    pass\n",
                encoding="utf-8",
            )
            (project_root / "src" / "domain" / "logic.py").write_text(
                "from src.domain.helpers import DEFAULT_REGION\n\n"
                "DEFAULT_TIMEOUT = 30\n"
                "DEFAULT_FLAGS = {'cache': True, 'retry_count': 3}\n\n"
                "def build_settings(timeout: int = DEFAULT_TIMEOUT) -> dict[str, object]:\n"
                "    return {\n"
                "        'region': DEFAULT_REGION,\n"
                "        'timeout': timeout,\n"
                "        'flags': DEFAULT_FLAGS,\n"
                "    }\n",
                encoding="utf-8",
            )
            (project_root / "agentic" / "agentic.yaml").write_text(
                "language: python\n"
                "exclusions:\n"
                "  - agentic/\n"
                "rules:\n"
                "  boundaries:\n"
                "    - source: src/domain\n"
                "      disallow:\n"
                "        - src/infra\n",
                encoding="utf-8",
            )

            result = run_architecture_check(project_root)

            self.assertEqual(result.files_found, 3)
            self.assertEqual(result.files_checked, 3)
            self.assertEqual(result.violations, [])

    def test_swallowed_errors_and_none_fallbacks_do_not_create_false_positive_violations(self) -> None:
        with TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            (project_root / "src" / "domain").mkdir(parents=True)
            (project_root / "src" / "infra").mkdir(parents=True)
            (project_root / "agentic").mkdir()

            (project_root / "src" / "domain" / "helpers.py").write_text(
                "def trim(value: str) -> str:\n"
                "    return value.strip()\n",
                encoding="utf-8",
            )
            (project_root / "src" / "infra" / "database.py").write_text(
                "class Database:\n    pass\n",
                encoding="utf-8",
            )
            (project_root / "src" / "domain" / "logic.py").write_text(
                "from src.domain.helpers import trim\n\n"
                "def normalize(raw: str | None) -> str | None:\n"
                "    if raw is None:\n"
                "        return None\n\n"
                "    try:\n"
                "        return trim(raw)\n"
                "    except ValueError:\n"
                "        return None\n",
                encoding="utf-8",
            )
            (project_root / "agentic" / "agentic.yaml").write_text(
                "language: python\n"
                "exclusions:\n"
                "  - agentic/\n"
                "rules:\n"
                "  boundaries:\n"
                "    - source: src/domain\n"
                "      disallow:\n"
                "        - src/infra\n",
                encoding="utf-8",
            )

            result = run_architecture_check(project_root)

            self.assertEqual(result.files_found, 3)
            self.assertEqual(result.files_checked, 3)
            self.assertEqual(result.violations, [])

    def test_literal_default_arguments_do_not_create_false_positive_violations(self) -> None:
        with TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            (project_root / "src" / "domain").mkdir(parents=True)
            (project_root / "src" / "infra").mkdir(parents=True)
            (project_root / "agentic").mkdir()

            (project_root / "src" / "domain" / "helpers.py").write_text(
                "def prefix(value: str) -> str:\n"
                "    return f'item:{value}'\n",
                encoding="utf-8",
            )
            (project_root / "src" / "infra" / "database.py").write_text(
                "class Database:\n    pass\n",
                encoding="utf-8",
            )
            (project_root / "src" / "domain" / "logic.py").write_text(
                "from src.domain.helpers import prefix\n\n"
                "def build_identifier(name: str = 'guest', retries: int = 2, enabled: bool = True) -> str:\n"
                "    if not enabled:\n"
                "        return name\n"
                "    return prefix(f'{name}-{retries}')\n",
                encoding="utf-8",
            )
            (project_root / "agentic" / "agentic.yaml").write_text(
                "language: python\n"
                "exclusions:\n"
                "  - agentic/\n"
                "rules:\n"
                "  boundaries:\n"
                "    - source: src/domain\n"
                "      disallow:\n"
                "        - src/infra\n",
                encoding="utf-8",
            )

            result = run_architecture_check(project_root)

            self.assertEqual(result.files_found, 3)
            self.assertEqual(result.files_checked, 3)
            self.assertEqual(result.violations, [])

    def test_glob_rule_allows_exact_public_feature_root_imports(self) -> None:
        with TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            (project_root / "src" / "features" / "orders").mkdir(parents=True)
            (project_root / "src" / "features" / "billing").mkdir(parents=True)
            (project_root / "agentic").mkdir()

            (project_root / "src" / "features" / "orders" / "service.py").write_text(
                "from src.features.billing import api\n",
                encoding="utf-8",
            )
            (project_root / "agentic" / "agentic.yaml").write_text(
                "language: python\n"
                "rules:\n"
                "  boundaries:\n"
                "    - source: src/features/*\n"
                "      disallow:\n"
                "        - src/features/*\n"
                "      allow_same_match: true\n"
                "      allow:\n"
                "        - src/features/*\n",
                encoding="utf-8",
            )

            result = run_architecture_check(project_root)

            self.assertEqual(result.violations, [])

    def test_exclusions_support_glob_patterns(self) -> None:
        with TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            (project_root / "src" / "generated" / "client").mkdir(parents=True)
            (project_root / "agentic").mkdir()

            (project_root / "src" / "generated" / "client" / "api.py").write_text(
                "from src.infra.database import Database\n",
                encoding="utf-8",
            )
            (project_root / "agentic" / "agentic.yaml").write_text(
                "language: python\n"
                "exclusions:\n"
                "  - src/generated/**\n"
                "rules:\n"
                "  boundaries:\n"
                "    - source: src/generated\n"
                "      disallow:\n"
                "        - src/infra\n",
                encoding="utf-8",
            )

            result = run_architecture_check(project_root)

            self.assertEqual(result.violations, [])

    def test_reports_syntax_errors_in_python_sources_instead_of_skipping_them(self) -> None:
        with TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            (project_root / "src" / "domain").mkdir(parents=True)
            (project_root / "agentic").mkdir()

            (project_root / "src" / "domain" / "logic.py").write_text(
                "def broken(:\n    pass\n",
                encoding="utf-8",
            )
            (project_root / "agentic" / "agentic.yaml").write_text(
                "language: python\nrules:\n  boundaries: []\n",
                encoding="utf-8",
            )

            with self.assertRaises(CheckerError) as context:
                run_architecture_check(project_root)

            self.assertIn("Extractor failed to analyze Python files",
                          str(context.exception))
            self.assertIn("src/domain/logic.py", str(context.exception))
            self.assertIn("SyntaxError", str(context.exception))

    def test_reports_invalid_utf8_python_sources_instead_of_skipping_them(self) -> None:
        with TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            (project_root / "src" / "domain").mkdir(parents=True)
            (project_root / "agentic").mkdir()

            (project_root / "src" / "domain" /
             "logic.py").write_bytes(b"\xff\xfe\x00")
            (project_root / "agentic" / "agentic.yaml").write_text(
                "language: python\nrules:\n  boundaries: []\n",
                encoding="utf-8",
            )

            with self.assertRaises(CheckerError) as context:
                run_architecture_check(project_root)

            self.assertIn("Extractor failed to analyze Python files",
                          str(context.exception))
            self.assertIn("src/domain/logic.py", str(context.exception))
            self.assertIn("UnicodeDecodeError", str(context.exception))

    def test_reports_typescript_read_failures_instead_of_skipping_them(self) -> None:
        if shutil.which("node") is None:
            self.skipTest("node runtime not available")

        with TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            source_dir = project_root / "src" / "domain"
            source_dir.mkdir(parents=True)
            (project_root / "agentic").mkdir()

            unreadable_path = source_dir / "logic.ts"
            unreadable_path.write_text(
                "export function broken(): string { return 'x'; }\n",
                encoding="utf-8",
            )
            unreadable_path.chmod(0)
            (project_root / "agentic" / "agentic.yaml").write_text(
                "language: typescript\nrules:\n  boundaries: []\n",
                encoding="utf-8",
            )

            try:
                with self.assertRaises(CheckerError) as context:
                    run_architecture_check(project_root)
            finally:
                unreadable_path.chmod(0o644)

            self.assertIn(
                "Extractor failed to analyze TypeScript files", str(context.exception))
            self.assertIn("src/domain/logic.ts", str(context.exception))

    def test_reports_php_syntax_errors_instead_of_skipping_them(self) -> None:
        if shutil.which("php") is None:
            self.skipTest("php runtime not available")

        with TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            (project_root / "src" / "domain").mkdir(parents=True)
            (project_root / "agentic").mkdir()

            (project_root / "src" / "domain" / "logic.php").write_text(
                "<?php\nfunction broken( {\n",
                encoding="utf-8",
            )
            (project_root / "agentic" / "agentic.yaml").write_text(
                "language: php\nrules:\n  boundaries: []\n",
                encoding="utf-8",
            )

            with self.assertRaises(CheckerError) as context:
                run_architecture_check(project_root)

            self.assertIn("Extractor failed to analyze PHP files",
                          str(context.exception))
            self.assertIn("src/domain/logic.php", str(context.exception))
            self.assertIn("ParseError", str(context.exception))


if __name__ == "__main__":
    unittest.main()
