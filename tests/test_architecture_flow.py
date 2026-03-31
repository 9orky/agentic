import json
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import Mock, patch
import unittest

from agentic.features.architecture_check import run_architecture_check


class ArchitectureFlowTests(unittest.TestCase):
    @patch("agentic.features.architecture_check.dependency_map.infrastructure.extractor_runtime.subprocess.run")
    def test_forward_only_flow_passes(self, mock_run: Mock) -> None:
        with TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            (project_root / "agentic").mkdir()

            mock_run.return_value = _mock_extractor_output(
                {
                    "src/features/order/api.py": {
                        "imports": ["src/modules/payment/service.py"],
                        "classes": [],
                        "functions": [],
                    },
                    "src/modules/payment/service.py": {
                        "imports": ["src/adapters/stripe/client.py"],
                        "classes": [],
                        "functions": [],
                    },
                    "src/adapters/stripe/client.py": {
                        "imports": [],
                        "classes": ["StripeClient"],
                        "functions": [],
                    },
                }
            )
            _write_flow_config(
                project_root,
                analyzers=["backward-flow", "no-reentry", "no-cycles"],
            )

            result = run_architecture_check(project_root)

            self.assertEqual(result.violations, [])

    @patch("agentic.features.architecture_check.dependency_map.infrastructure.extractor_runtime.subprocess.run")
    def test_detects_backward_flow(self, mock_run: Mock) -> None:
        with TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            (project_root / "agentic").mkdir()

            mock_run.return_value = _mock_extractor_output(
                {
                    "src/modules/payment/service.py": {
                        "imports": ["src/features/order/api.py"],
                        "classes": [],
                        "functions": [],
                    },
                    "src/features/order/api.py": {
                        "imports": [],
                        "classes": [],
                        "functions": ["create_order"],
                    },
                }
            )
            _write_flow_config(project_root, analyzers=["backward-flow"])

            result = run_architecture_check(project_root)

            self.assertEqual(len(result.violations), 1)
            self.assertIn("backward-flow", result.violations[0])
            self.assertIn("src/features/order/api", result.violations[0])

    @patch("agentic.features.architecture_check.dependency_map.infrastructure.extractor_runtime.subprocess.run")
    def test_detects_module_reentry(self, mock_run: Mock) -> None:
        with TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            (project_root / "agentic").mkdir()

            mock_run.return_value = _mock_extractor_output(
                {
                    "src/features/order/api.py": {
                        "imports": ["src/modules/payment/service.py"],
                        "classes": [],
                        "functions": [],
                    },
                    "src/modules/payment/service.py": {
                        "imports": ["src/adapters/stripe/client.py"],
                        "classes": [],
                        "functions": [],
                    },
                    "src/adapters/stripe/client.py": {
                        "imports": ["src/modules/user/service.py"],
                        "classes": [],
                        "functions": [],
                    },
                    "src/modules/user/service.py": {
                        "imports": [],
                        "classes": ["UserService"],
                        "functions": [],
                    },
                }
            )
            _write_flow_config(project_root, analyzers=["no-reentry"])

            result = run_architecture_check(project_root)

            self.assertEqual(len(result.violations), 1)
            self.assertIn("no-reentry", result.violations[0])
            self.assertIn("src/modules/user/service", result.violations[0])

    @patch("agentic.features.architecture_check.dependency_map.infrastructure.extractor_runtime.subprocess.run")
    def test_detects_module_cycle(self, mock_run: Mock) -> None:
        with TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            (project_root / "agentic").mkdir()

            mock_run.return_value = _mock_extractor_output(
                {
                    "src/modules/payment/service.py": {
                        "imports": ["src/modules/user/service.py"],
                        "classes": [],
                        "functions": [],
                    },
                    "src/modules/user/service.py": {
                        "imports": ["src/modules/payment/service.py"],
                        "classes": [],
                        "functions": [],
                    },
                }
            )
            _write_flow_config(project_root, analyzers=["no-cycles"])

            result = run_architecture_check(project_root)

            self.assertEqual(len(result.violations), 1)
            self.assertIn("no-cycles", result.violations[0])
            self.assertIn("src/modules/payment/service", result.violations[0])
            self.assertIn("src/modules/user/service", result.violations[0])


def _write_flow_config(project_root: Path, *, analyzers: list[str]) -> None:
    (project_root / "agentic" / "agentic.yaml").write_text(
        "language: python\n"
        "rules:\n"
        "  boundaries: []\n"
        "  tags:\n"
        "    - name: feature\n"
        "      match: src/features/**\n"
        "    - name: module\n"
        "      match: src/modules/**\n"
        "    - name: adapter\n"
        "      match: src/adapters/**\n"
        "  flow:\n"
        "    layers:\n"
        "      - feature\n"
        "      - module\n"
        "      - adapter\n"
        "    module_tag: module\n"
        f"    analyzers: [{', '.join(repr(name) for name in analyzers)}]\n",
        encoding="utf-8",
    )


def _mock_extractor_output(files: dict[str, dict[str, list[str]]]) -> Mock:
    return Mock(
        stdout=json.dumps(
            {
                "files": files,
                "summary": {
                    "files_found": len(files),
                    "files_excluded": 0,
                    "files_checked": len(files),
                },
            }
        ),
        stderr="",
        returncode=0,
    )


if __name__ == "__main__":
    unittest.main()
