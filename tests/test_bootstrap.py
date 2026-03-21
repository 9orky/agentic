from importlib.resources import files
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from agentic.features.workspace_contract import bootstrap_project, update_project


EXPECTED_SHARED_RULE_PATHS = (
    Path("rules") / "AGENT.md",
    Path("rules") / "feature" / "FEATURE.md",
    Path("rules") / "feature" / "layers" / "DOMAIN.md",
    Path("rules") / "feature" / "layers" / "INFRASTRUCTURE.md",
    Path("rules") / "feature" / "layers" / "APPLICATION.md",
    Path("rules") / "feature" / "layers" / "UI.md",
    Path("rules") / "module" / "MODULE.md",
    Path("rules") / "planning" / "PLANNING.md",
    Path("rules") / "planning" / "phases" / "BIG_PICTURE.md",
    Path("rules") / "planning" / "phases" / "STEPS.md",
    Path("rules") / "refactoring" / "REFACTORING.md",
    Path("rules") / "tests" / "TESTS.md",
)


class BootstrapProjectTests(unittest.TestCase):
    def test_bootstrap_creates_local_agentic_folder(self) -> None:
        with TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)

            result = bootstrap_project(project_root)

            self.assertTrue(result.created_dir)
            self.assertTrue(
                (project_root / "agentic" / "agentic.yaml").exists())
            for relative_path in EXPECTED_SHARED_RULE_PATHS:
                self.assertTrue(
                    (project_root / "agentic" / relative_path).exists())
            self.assertTrue((project_root / "agentic" /
                            "rules" / "overrides").is_dir())
            self.assertTrue((project_root / "agentic" /
                            "rules" / "project-specific").is_dir())
            self.assertFalse((project_root / "agentic" / "guide").exists())
            self.assertFalse((project_root / "agentic" / "reference").exists())

    def test_bootstrap_preserves_existing_files(self) -> None:
        with TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            bootstrap_project(project_root)

            config_path = project_root / "agentic" / "agentic.yaml"
            config_path.write_text("language: php\n", encoding="utf-8")

            result = bootstrap_project(project_root)

            self.assertFalse(result.created_dir)
            self.assertIn(config_path, result.preserved_files)
            self.assertEqual(config_path.read_text(
                encoding="utf-8"), "language: php\n")

    def test_update_overwrites_shared_docs_and_preserves_local_state(self) -> None:
        with TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            bootstrap_project(project_root)

            shared_doc_path = project_root / "agentic" / "rules" / "AGENT.md"
            config_path = project_root / "agentic" / "agentic.yaml"
            project_specific_path = project_root / "agentic" / \
                "rules" / "project-specific" / "LOCAL.md"
            override_path = project_root / "agentic" / \
                "rules" / "overrides" / "TESTS.md"
            project_specific_path.write_text("local note\n", encoding="utf-8")
            override_path.write_text("local override\n", encoding="utf-8")

            shared_doc_path.write_text(
                "locally modified shared doc\n", encoding="utf-8")
            config_path.write_text("language: php\n", encoding="utf-8")

            result = update_project(project_root)

            self.assertIn(shared_doc_path, result.updated_files)
            self.assertIn(config_path, result.preserved_files)
            self.assertEqual(shared_doc_path.read_text(
                encoding="utf-8"),
                files("agentic").joinpath("resources", "rules",
                                          "AGENT.md").read_text(encoding="utf-8"),
            )
            self.assertEqual(config_path.read_text(
                encoding="utf-8"), "language: php\n")
            self.assertEqual(project_specific_path.read_text(
                encoding="utf-8"), "local note\n")
            self.assertEqual(override_path.read_text(
                encoding="utf-8"), "local override\n")

    def test_update_marks_unchanged_shared_docs_as_updated(self) -> None:
        with TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            bootstrap_project(project_root)

            shared_doc_path = project_root / "agentic" / "rules" / "AGENT.md"

            result = update_project(project_root)

            self.assertIn(shared_doc_path, result.updated_files)
            self.assertNotIn(shared_doc_path, result.preserved_files)


if __name__ == "__main__":
    unittest.main()
