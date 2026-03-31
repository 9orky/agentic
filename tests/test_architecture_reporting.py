import json
import agentic.features.architecture_check.dependency_map.infrastructure as architecture_dependency_map_infrastructure
import agentic.features.architecture_check.dependency_map.infrastructure.extractor_registry as architecture_dependency_map_extractor_registry
import agentic.features.architecture_check.dependency_map.infrastructure.extractor_runtime as architecture_dependency_map_extractor_runtime
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import Mock, patch
import unittest

from agentic.cli import main


class ArchitectureCheckInfrastructurePackageTests(unittest.TestCase):
    def test_infrastructure_package_exports_expected_public_seam(self) -> None:
        self.assertEqual(
            architecture_dependency_map_infrastructure.__all__,
            [
                "ConfigLoader",
                "ExtractorRuntime",
                "ExtractorRuntimeFactory",
                "ExtractorSpecRegistry",
                "SubprocessExtractorRuntime",
            ],
        )

    def test_infrastructure_package_does_not_reexport_anchor_internal_spec_type(self) -> None:
        self.assertFalse(
            hasattr(architecture_dependency_map_infrastructure, "ExtractorSpec"))

    def test_extractor_registry_anchor_exports_expected_public_seam(self) -> None:
        self.assertEqual(
            architecture_dependency_map_extractor_registry.__all__,
            ["ExtractorSpec", "ExtractorSpecRegistry"],
        )

    def test_extractor_runtime_anchor_exports_expected_public_seam(self) -> None:
        self.assertEqual(
            architecture_dependency_map_extractor_runtime.__all__,
            ["ExtractorRuntime", "SubprocessExtractorRuntime"],
        )

    def test_infrastructure_directory_matches_allowed_anchor_shape(self) -> None:
        infrastructure_dir = Path(
            architecture_dependency_map_infrastructure.__file__).resolve().parent
        entries = {
            path.name
            for path in infrastructure_dir.iterdir()
            if path.name != "__pycache__"
        }

        self.assertEqual(
            entries,
            {
                "__init__.py",
                "config_loader.py",
                "extractor_runtime_factory.py",
                "extractor_registry",
                "extractor_runtime",
            },
        )

    def test_infrastructure_runtime_factory_creates_subprocess_runtime(self) -> None:
        runtime = architecture_dependency_map_infrastructure.ExtractorRuntimeFactory().create()

        self.assertIsInstance(
            runtime,
            architecture_dependency_map_infrastructure.SubprocessExtractorRuntime,
        )


class ArchitectureReportingTests(unittest.TestCase):
    @patch("agentic.features.architecture_check.dependency_map.infrastructure.extractor_runtime.subprocess.run")
    def test_check_command_groups_flow_violations_in_text_output(self, mock_run: Mock) -> None:
        with TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            (project_root / "agentic").mkdir()
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
                "    analyzers: ['no-reentry']\n",
                encoding="utf-8",
            )
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
                        "classes": [],
                        "functions": [],
                    },
                }
            )

            output = StringIO()
            with redirect_stdout(output):
                exit_code = main(
                    ["check", "--project-root", str(project_root)])

            self.assertEqual(exit_code, 1)
            rendered = output.getvalue()
            self.assertIn("No Re-Entry Violations:", rendered)
            self.assertIn(
                "src/features/order/api.py -> src/modules/payment/service.py -> src/adapters/stripe/client.py -> [src/modules/user/service.py]  no-reentry", rendered)

    @patch("agentic.features.architecture_check.dependency_map.infrastructure.extractor_runtime.subprocess.run")
    def test_check_command_supports_json_output(self, mock_run: Mock) -> None:
        with TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            (project_root / "src" / "domain").mkdir(parents=True)
            (project_root / "src" / "infra").mkdir(parents=True)
            (project_root / "agentic").mkdir()
            (project_root / "src" / "domain" /
             "logic.py").write_text("x\n", encoding="utf-8")
            (project_root / "agentic" / "agentic.yaml").write_text(
                "language: python\n"
                "rules:\n"
                "  boundaries:\n"
                "    - source: src/domain\n"
                "      disallow:\n"
                "        - src/infra\n",
                encoding="utf-8",
            )
            mock_run.return_value = _mock_extractor_output(
                {
                    "src/domain/logic.py": {
                        "imports": ["src/infra/database.py"],
                        "classes": [],
                        "functions": [],
                    },
                    "src/infra/database.py": {
                        "imports": [],
                        "classes": [],
                        "functions": [],
                    },
                }
            )

            output = StringIO()
            with redirect_stdout(output):
                exit_code = main(["check", "--project-root",
                                 str(project_root), "--output", "json"])

            self.assertEqual(exit_code, 1)
            payload = json.loads(output.getvalue())
            self.assertEqual(payload["files_checked"], 2)
            self.assertEqual(payload["violations"][0]["type"], "edge-rule")
            self.assertEqual(payload["violations"][0]["path"], [
                             "src/domain/logic.py", "src/infra/database.py"])

    @patch("agentic.features.architecture_check.dependency_map.infrastructure.extractor_runtime.subprocess.run")
    def test_check_command_writes_dot_for_violating_paths(self, mock_run: Mock) -> None:
        with TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            dot_path = project_root / "violations.dot"
            (project_root / "agentic").mkdir()
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
                "    analyzers: ['backward-flow']\n",
                encoding="utf-8",
            )
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
                        "functions": [],
                    },
                }
            )

            output = StringIO()
            with redirect_stdout(output):
                exit_code = main([
                    "check",
                    "--project-root",
                    str(project_root),
                    "--dot",
                    str(dot_path),
                ])

            self.assertEqual(exit_code, 1)
            self.assertTrue(dot_path.exists())
            dot_text = dot_path.read_text(encoding="utf-8")
            self.assertIn(
                '"src/modules/payment/service.py" -> "src/features/order/api.py";', dot_text)


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
