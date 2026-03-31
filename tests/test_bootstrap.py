from importlib.resources import files
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from agentic.features.workspace_contract import bootstrap_project, update_project


def _expected_shared_rule_paths() -> tuple[Path, ...]:
    rules_root = files("agentic").joinpath("resources", "rules")
    return tuple(
        Path("rules") / relative_path
        for relative_path in _iter_packaged_rule_paths(rules_root, Path())
    )


def _iter_packaged_rule_paths(directory, relative_path: Path):
    for child in sorted(directory.iterdir(), key=lambda item: item.name):
        child_relative_path = relative_path / child.name
        if child.is_dir():
            if child.name in {"overrides", "project-specific"}:
                continue
            yield from _iter_packaged_rule_paths(child, child_relative_path)
            continue

        if child.name.startswith("."):
            continue
        if child_relative_path.suffix != ".md":
            continue

        yield child_relative_path


class BootstrapProjectTests(unittest.TestCase):
    def test_bootstrap_creates_local_agentic_folder(self) -> None:
        with TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)

            result = bootstrap_project(project_root)

            self.assertTrue(result.created_dir)
            self.assertTrue(
                (project_root / "agentic" / "agentic.yaml").exists())
            self.assertTrue(
                (project_root / ".github" / "copilot-instructions.md").exists())
            for relative_path in _expected_shared_rule_paths():
                self.assertTrue(
                    (project_root / "agentic" / relative_path).exists())
            self.assertFalse((project_root / "agentic" / "guide").exists())
            self.assertFalse((project_root / "agentic" / "reference").exists())
            self.assertEqual(
                (project_root / ".github" /
                 "copilot-instructions.md").read_text(encoding="utf-8"),
                files("agentic").joinpath("resources",
                                          "copilot-instructions.md").read_text(encoding="utf-8"),
            )

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

            shared_doc_path = project_root / "agentic" / "rules" / "INDEX.md"
            config_path = project_root / "agentic" / "agentic.yaml"
            bootstrap_instruction_path = project_root / \
                ".github" / "copilot-instructions.md"

            shared_doc_path.write_text(
                "locally modified shared doc\n", encoding="utf-8")
            config_path.write_text("language: php\n", encoding="utf-8")
            bootstrap_instruction_path.write_text("junk\n", encoding="utf-8")

            result = update_project(project_root)

            self.assertIn(shared_doc_path, result.updated_files)
            self.assertIn(bootstrap_instruction_path, result.updated_files)
            self.assertIn(config_path, result.preserved_files)
            self.assertEqual(shared_doc_path.read_text(
                encoding="utf-8"),
                files("agentic").joinpath("resources", "rules",
                                          "INDEX.md").read_text(encoding="utf-8"),
            )
            self.assertEqual(
                bootstrap_instruction_path.read_text(encoding="utf-8"),
                files("agentic").joinpath("resources",
                                          "copilot-instructions.md").read_text(encoding="utf-8"),
            )
            self.assertEqual(config_path.read_text(
                encoding="utf-8"), "language: php\n")

    def test_update_preserves_unchanged_shared_docs(self) -> None:
        with TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            bootstrap_project(project_root)

            shared_doc_path = project_root / "agentic" / "rules" / "INDEX.md"

            result = update_project(project_root)

            self.assertNotIn(shared_doc_path, result.updated_files)
            self.assertIn(shared_doc_path, result.preserved_files)


if __name__ == "__main__":
    unittest.main()
