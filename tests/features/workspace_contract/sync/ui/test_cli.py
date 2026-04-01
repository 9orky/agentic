from __future__ import annotations

import random
import tempfile
import unittest
from importlib.resources import files
from pathlib import Path
from unittest.mock import patch

from click.testing import CliRunner

from agentic.cli import agentic_cli


class SyncCliFunctionalTests(unittest.TestCase):
    def setUp(self) -> None:
        self._temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self._temp_dir.cleanup)
        self.project_root = Path(self._temp_dir.name)
        self.runner = CliRunner()

    def test_init_mirrors_packaged_rule_tree_without_hardcoded_manifest(self) -> None:
        packaged_snapshot = _snapshot_packaged_rules()

        result = self._invoke_from_mocked_cwd(["init"])

        self.assertEqual(result.exit_code, 0, result.output)
        self.assertEqual(
            _snapshot_path_tree(self.project_root / "agentic" / "rules"),
            packaged_snapshot,
        )

    def test_update_rewrites_only_mutated_rule_files(self) -> None:
        packaged_before = _snapshot_packaged_rules()
        init_result = self._invoke_from_mocked_cwd(["init"])
        self.assertEqual(init_result.exit_code, 0, init_result.output)

        rule_root = self.project_root / "agentic" / "rules"
        mirrored_paths = sorted(
            path.relative_to(rule_root)
            for path in rule_root.rglob("*.md")
        )
        self.assertTrue(mirrored_paths)

        randomizer = random.Random(7)
        sample_size = max(1, len(mirrored_paths) // 4)
        selected_paths = set(randomizer.sample(mirrored_paths, sample_size))

        for relative_path in selected_paths:
            target_path = rule_root / relative_path
            target_path.write_text(
                target_path.read_text(encoding="utf-8") +
                "\nlocal test mutation\n",
                encoding="utf-8",
            )

        update_result = self._invoke_from_mocked_cwd(["update"])

        self.assertEqual(update_result.exit_code, 0, update_result.output)
        self.assertEqual(_snapshot_packaged_rules(), packaged_before)
        self.assertEqual(_snapshot_path_tree(rule_root), packaged_before)
        self.assertEqual(
            _reported_rule_update_paths(update_result.output),
            {
                (Path("agentic") / "rules" / relative_path).as_posix()
                for relative_path in selected_paths
            },
        )

    def _invoke_from_mocked_cwd(self, args: list[str]):
        with patch(
            "agentic.cli.Path.cwd",
            return_value=self.project_root,
        ):
            return self.runner.invoke(agentic_cli, args, catch_exceptions=False)


def _snapshot_packaged_rules() -> dict[str, str]:
    return _snapshot_traversable_tree(files("agentic").joinpath("resources", "rules"))


def _snapshot_traversable_tree(root, relative_path: Path = Path()) -> dict[str, str]:
    snapshot: dict[str, str] = {}
    for child in sorted(root.iterdir(), key=lambda item: item.name):
        child_relative_path = relative_path / child.name
        if child.is_dir():
            snapshot.update(_snapshot_traversable_tree(
                child, child_relative_path))
            continue

        snapshot[child_relative_path.as_posix()] = child.read_text(
            encoding="utf-8")
    return snapshot


def _snapshot_path_tree(root: Path) -> dict[str, str]:
    snapshot: dict[str, str] = {}
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        snapshot[path.relative_to(root).as_posix()
                 ] = path.read_text(encoding="utf-8")
    return snapshot


def _reported_rule_update_paths(output: str) -> set[str]:
    return {
        line[2:]
        for line in output.splitlines()
        if line.startswith("- agentic/rules/")
    }


if __name__ == "__main__":
    unittest.main()
