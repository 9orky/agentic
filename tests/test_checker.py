import json
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import Mock, patch
import unittest

from agentic.features.architecture_check import CheckerError, run_architecture_check


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


if __name__ == "__main__":
    unittest.main()
