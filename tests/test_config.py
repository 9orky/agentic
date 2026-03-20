from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from agentic.features.configuration import load_config


class ConfigTests(unittest.TestCase):
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


if __name__ == "__main__":
    unittest.main()
