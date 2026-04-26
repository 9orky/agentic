from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path

from click.testing import CliRunner

from agentic.cli import agentic_cli


class CodeCliTests(unittest.TestCase):
    def setUp(self) -> None:
        self.runner = CliRunner()
        self._temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self._temp_dir.cleanup)
        self.project_root = Path(self._temp_dir.name)

    def test_code_command_generates_recipe_tree_in_current_directory(self) -> None:
        recipe_dir = self.project_root / "agentic" / "code" / "feature"
        (recipe_dir / "module" / "domain").mkdir(parents=True)
        (recipe_dir / "module" / "domain" / "entity.py").write_text(
            "class Entity: ...\n",
            encoding="utf-8",
        )

        target_dir = self.project_root / "src" / "feature_mod"
        target_dir.mkdir(parents=True)

        result = self._invoke_from_cwd(target_dir, ["code", "feature"])

        self.assertEqual(result.exit_code, 0, result.output)
        self.assertTrue((target_dir / "module").is_dir())
        self.assertTrue(
            (target_dir / "module" / "domain" / "entity.py").is_file())
        self.assertIn("Generated recipe 'feature'.", result.output)
        self.assertIn("Created 3 path(s).", result.output)
        self.assertIn("- module/domain/entity.py", result.output)

    def test_code_command_dry_run_reports_changes_without_mutation(self) -> None:
        recipe_dir = self.project_root / "agentic" / "code" / "feature"
        (recipe_dir / "module" / "domain").mkdir(parents=True)
        (recipe_dir / "module" / "domain" / "entity.py").write_text(
            "class Entity: ...\n",
            encoding="utf-8",
        )

        target_dir = self.project_root / "src" / "feature_mod"
        target_dir.mkdir(parents=True)

        result = self._invoke_from_cwd(
            target_dir, ["code", "feature", "--dry-run"])

        self.assertEqual(result.exit_code, 0, result.output)
        self.assertFalse((target_dir / "module").exists())
        self.assertIn("Dry run for recipe 'feature'.", result.output)
        self.assertIn("Would create 3 path(s).", result.output)

    def test_code_command_returns_error_for_missing_recipe(self) -> None:
        target_dir = self.project_root / "src" / "feature_mod"
        target_dir.mkdir(parents=True)

        result = self._invoke_from_cwd(target_dir, ["code", "missing"])

        self.assertEqual(result.exit_code, 1, result.output)
        self.assertIn(
            "Recipe not found: agentic/code/missing/.", result.output)

    def test_code_command_renders_empty_recipe_warning(self) -> None:
        (self.project_root / "agentic" / "code" / "feature").mkdir(parents=True)
        target_dir = self.project_root / "src" / "feature_mod"
        target_dir.mkdir(parents=True)

        result = self._invoke_from_cwd(target_dir, ["code", "feature"])

        self.assertEqual(result.exit_code, 0, result.output)
        self.assertIn("No changes.", result.output)
        self.assertIn("Warning: recipe 'feature' is empty.", result.output)

    def test_code_command_loads_recipe_from_enclosing_project_root(self) -> None:
        recipe_dir = self.project_root / "agentic" / "code" / "layers" / "domain"
        recipe_dir.mkdir(parents=True)
        (recipe_dir / "entity.py").write_text("class Entity: ...\n", encoding="utf-8")

        nested_cwd = self.project_root / "src" / "agentic" / \
            "features" / "workspace_contract" / "testmod"
        nested_cwd.mkdir(parents=True)

        result = self._invoke_from_cwd(nested_cwd, ["code", "layers"])

        self.assertEqual(result.exit_code, 0, result.output)
        self.assertTrue((nested_cwd / "domain").is_dir())
        self.assertTrue((nested_cwd / "domain" / "entity.py").is_file())
        self.assertIn("Generated recipe 'layers'.", result.output)

    def test_code_command_loads_recipe_from_hidden_agentic_directory(self) -> None:
        recipe_dir = self.project_root / ".agentic" / "code" / "layers" / "domain"
        recipe_dir.mkdir(parents=True)
        (recipe_dir / "entity.py").write_text("class Entity: ...\n", encoding="utf-8")

        nested_cwd = self.project_root / "src" / "agentic" / \
            "features" / "workspace_contract" / "testmod"
        nested_cwd.mkdir(parents=True)

        result = self._invoke_from_cwd(nested_cwd, ["code", "layers"])

        self.assertEqual(result.exit_code, 0, result.output)
        self.assertTrue((nested_cwd / "domain").is_dir())
        self.assertTrue((nested_cwd / "domain" / "entity.py").is_file())
        self.assertIn("Generated recipe 'layers'.", result.output)

    def test_code_command_fails_when_both_agentic_directories_exist(self) -> None:
        (self.project_root / "agentic" / "code" /
         "layers" / "domain").mkdir(parents=True)
        (self.project_root / ".agentic" / "code" /
         "layers" / "domain").mkdir(parents=True)
        target_dir = self.project_root / "src" / "feature_mod"
        target_dir.mkdir(parents=True)

        result = self._invoke_from_cwd(target_dir, ["code", "layers"])

        self.assertEqual(result.exit_code, 1, result.output)
        self.assertIn(
            "Error: Found multiple agentic directories: agentic, .agentic. Delete one of them and rerun agentic.",
            result.output,
        )

    def test_code_command_preserves_existing_paths_and_reports_skips(self) -> None:
        recipe_dir = self.project_root / "agentic" / "code" / "feature"
        recipe_dir.mkdir(parents=True)
        (recipe_dir / "entity.py").write_text("from recipe\n", encoding="utf-8")

        target_dir = self.project_root / "src" / "feature_mod"
        target_dir.mkdir(parents=True)
        (target_dir / "entity.py").write_text("local change\n", encoding="utf-8")

        result = self._invoke_from_cwd(target_dir, ["code", "feature"])

        self.assertEqual(result.exit_code, 0, result.output)
        self.assertIn("Skipped 1 path(s).", result.output)
        self.assertEqual(
            (target_dir / "entity.py").read_text(encoding="utf-8"), "local change\n")

    def test_code_command_skips_paths_matching_agentic_config_globs(self) -> None:
        recipe_dir = self.project_root / "agentic" / "code" / "feature"
        (recipe_dir / "module" / "__pycache__").mkdir(parents=True)
        (recipe_dir / "module" / "__pycache__" / "cache.pyc").write_text(
            "cached\n",
            encoding="utf-8",
        )
        (recipe_dir / "module" / "entity.py").write_text(
            "class Entity: ...\n",
            encoding="utf-8",
        )
        (self.project_root / "agentic" / "agentic.yaml").write_text(
            'code:\n  skip: ["*__pycache__*"]\n',
            encoding="utf-8",
        )

        target_dir = self.project_root / "src" / "feature_mod"
        target_dir.mkdir(parents=True)

        result = self._invoke_from_cwd(target_dir, ["code", "feature"])

        self.assertEqual(result.exit_code, 0, result.output)
        self.assertTrue((target_dir / "module" / "entity.py").is_file())
        self.assertFalse((target_dir / "module" / "__pycache__").exists())
        self.assertIn("Skipped 2 path(s).", result.output)

    def test_code_command_dry_run_skips_paths_matching_agentic_config_globs(self) -> None:
        recipe_dir = self.project_root / "agentic" / "code" / "feature"
        (recipe_dir / "module" / "__pycache__").mkdir(parents=True)
        (recipe_dir / "module" / "__pycache__" / "cache.pyc").write_text(
            "cached\n",
            encoding="utf-8",
        )
        (recipe_dir / "module" / "entity.py").write_text(
            "class Entity: ...\n",
            encoding="utf-8",
        )
        (self.project_root / "agentic" / "agentic.yaml").write_text(
            'code:\n  skip: ["*__pycache__*"]\n',
            encoding="utf-8",
        )

        target_dir = self.project_root / "src" / "feature_mod"
        target_dir.mkdir(parents=True)

        result = self._invoke_from_cwd(
            target_dir, ["code", "feature", "--dry-run"])

        self.assertEqual(result.exit_code, 0, result.output)
        self.assertFalse((target_dir / "module").exists())
        self.assertIn("Would create 2 path(s).", result.output)
        self.assertIn("Skipped 2 path(s).", result.output)

    def test_code_command_generates_recipe_tree_in_requested_path(self) -> None:
        recipe_dir = self.project_root / "agentic" / "code" / "feature"
        (recipe_dir / "module" / "domain").mkdir(parents=True)
        (recipe_dir / "module" / "domain" / "entity.py").write_text(
            "class Entity: ...\n",
            encoding="utf-8",
        )

        target_dir = self.project_root / "src" / "feature_mod"
        target_dir.mkdir(parents=True)

        result = self._invoke_from_cwd(
            target_dir, ["code", "feature", "nested/output"])

        self.assertEqual(result.exit_code, 0, result.output)
        self.assertTrue((target_dir / "nested" / "output").is_dir())
        self.assertTrue(
            (target_dir / "nested" / "output" /
             "module" / "domain" / "entity.py").is_file()
        )
        self.assertIn("- nested/output/module/domain/entity.py", result.output)

    def _invoke_from_cwd(self, cwd: Path, args: list[str]):
        previous_cwd = Path.cwd()
        try:
            os.chdir(cwd)
            return self.runner.invoke(agentic_cli, args, catch_exceptions=False)
        finally:
            os.chdir(previous_cwd)


if __name__ == "__main__":
    unittest.main()
