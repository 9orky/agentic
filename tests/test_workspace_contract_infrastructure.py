from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from agentic.features.workspace_contract.domain import SharedRulePath, WorkspaceContractLayout
from agentic.features.workspace_contract.infrastructure import PackagedRulesReader, WorkspaceReader, WorkspaceWriter


class PackagedRulesReaderTests(unittest.TestCase):
    def test_iter_shared_rule_paths_reads_packaged_rules_tree(self) -> None:
        reader = PackagedRulesReader()

        shared_rule_paths = reader.iter_shared_rule_paths()
        rendered_paths = tuple(path.as_posix() for path in shared_rule_paths)

        self.assertIn("AGENT.md", rendered_paths)
        self.assertIn("planning/PLANNING.md", rendered_paths)
        self.assertIn("refactoring/REFACTORING.md", rendered_paths)
        self.assertEqual(rendered_paths, tuple(sorted(rendered_paths)))
        self.assertFalse(any(path.startswith("overrides/")
                         for path in rendered_paths))
        self.assertFalse(any(path.startswith("project-specific/")
                         for path in rendered_paths))

    def test_reads_packaged_rule_text_and_default_config(self) -> None:
        reader = PackagedRulesReader()

        self.assertIn("# Agent Rules", reader.read_document_text(
            SharedRulePath(Path("AGENT.md"))))
        self.assertIn("language:", reader.default_config_text())


class WorkspaceFilesystemAdapterTests(unittest.TestCase):
    def test_writer_creates_target_and_local_extension_directories(self) -> None:
        writer = WorkspaceWriter()
        layout = WorkspaceContractLayout()

        with TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)

            target_dir, created_dir = writer.ensure_target_directory(
                project_root, layout=layout)
            overrides_dir, project_specific_dir = writer.ensure_local_extension_directories(
                project_root, layout=layout)

            self.assertTrue(created_dir)
            self.assertEqual(target_dir, project_root / "agentic")
            self.assertTrue(overrides_dir.is_dir())
            self.assertTrue(project_specific_dir.is_dir())

    def test_reader_reports_existing_workspace_paths(self) -> None:
        reader = WorkspaceReader()
        writer = WorkspaceWriter()
        layout = WorkspaceContractLayout()

        with TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            writer.ensure_target_directory(project_root, layout=layout)
            writer.ensure_local_extension_directories(
                project_root, layout=layout)

            agent_document = layout.shared_rule_destination(
                project_root, SharedRulePath(Path("AGENT.md")))
            writer.write_text(agent_document, "agent rules\n")
            writer.write_text(layout.config_path(
                project_root), "language: python\n")
            override_path = layout.overrides_dir(project_root) / "TESTS.md"
            project_specific_path = layout.project_specific_dir(
                project_root) / "LOCAL.md"
            writer.write_text(override_path, "override\n")
            writer.write_text(project_specific_path, "local\n")

            self.assertTrue(reader.agentic_dir_exists(
                project_root, layout=layout))
            self.assertTrue(reader.config_exists(project_root, layout=layout))
            self.assertEqual(
                reader.existing_shared_rule_paths(
                    project_root,
                    [SharedRulePath(Path("planning") / "PLANNING.md"),
                     SharedRulePath(Path("AGENT.md"))],
                    layout=layout,
                ),
                (project_root / "agentic" / "rules" / "AGENT.md",),
            )
            self.assertEqual(reader.read_text(agent_document), "agent rules\n")
            self.assertEqual(reader.list_override_paths(
                project_root, layout=layout), (override_path,))
            self.assertEqual(reader.list_project_specific_paths(
                project_root, layout=layout), (project_specific_path,))

    def test_writer_rejects_file_in_place_of_target_directory(self) -> None:
        writer = WorkspaceWriter()

        with TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            (project_root / "agentic").write_text("not a directory\n", encoding="utf-8")

            with self.assertRaises(NotADirectoryError):
                writer.ensure_target_directory(project_root)


if __name__ == "__main__":
    unittest.main()
