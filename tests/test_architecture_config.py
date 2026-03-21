from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from agentic.features.architecture_check import load_config
from agentic.features.architecture_check.application.queries.load_config import LoadConfigQuery
from agentic.features.architecture_check.infrastructure import ConfigLoader
from agentic.project_layout import AgenticProjectLayout


class ArchitectureConfigTests(unittest.TestCase):
    def test_loads_yaml_config_from_agentic_directory(self) -> None:
        with TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            agentic_dir = project_root / "agentic"
            agentic_dir.mkdir()
            (agentic_dir / "agentic.yaml").write_text(
                "language: python\nexclusions:\n  - tests/\nrules:\n  boundaries: []\n",
                encoding="utf-8",
            )

            result = load_config(project_root)

            self.assertEqual(result.source_format, "yaml")
            self.assertEqual(result.config.language, "python")
            self.assertEqual(result.config.exclusions, ["tests/"])

    def test_loads_yaml_config_from_project_root(self) -> None:
        with TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            (project_root / "agentic.yaml").write_text(
                "language: php\nexclusions:\n  - vendor/**\nrules:\n  boundaries: []\n",
                encoding="utf-8",
            )

            result = load_config(project_root)

            self.assertEqual(result.source_format, "yaml")
            self.assertEqual(result.config.language, "php")
            self.assertEqual(result.config.exclusions, ["vendor/**"])

    def test_explicit_config_path_takes_precedence(self) -> None:
        with TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            default_config = project_root / "agentic.yaml"
            explicit_dir = project_root / "config"
            explicit_dir.mkdir()
            explicit_config = explicit_dir / "custom.yaml"

            default_config.write_text(
                "language: python\nrules:\n  boundaries: []\n",
                encoding="utf-8",
            )
            explicit_config.write_text(
                "language: typescript\nrules:\n  boundaries: []\n",
                encoding="utf-8",
            )

            result = load_config(project_root, str(explicit_config))

            self.assertEqual(result.path, explicit_config.resolve())
            self.assertEqual(result.config.language, "typescript")

    def test_load_query_can_use_shared_layout_override(self) -> None:
        with TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            custom_layout = AgenticProjectLayout(
                agentic_dir_name="workspace-contract",
                config_file_stem="ruleset",
            )
            managed_config = project_root / "workspace-contract" / "ruleset.yaml"
            managed_config.parent.mkdir()
            managed_config.write_text(
                "language: python\nrules:\n  boundaries: []\n",
                encoding="utf-8",
            )

            result = LoadConfigQuery(
                config_loader=ConfigLoader(layout=custom_layout)
            ).load(project_root)

            self.assertEqual(result.path, managed_config.resolve())
            self.assertEqual(result.config.language, "python")


if __name__ == "__main__":
    unittest.main()
