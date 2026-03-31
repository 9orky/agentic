import agentic.features.workspace_contract.rules.infrastructure as rules_infrastructure
import agentic.features.workspace_contract.workspace_sync.infrastructure as workspace_sync_infrastructure
import agentic.features.workspace_contract.workspace_sync.infrastructure.filesystem as workspace_sync_infrastructure_filesystem
import agentic.features.workspace_contract.workspace_sync.infrastructure.resources as workspace_sync_infrastructure_resources
import re
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from agentic.features.workspace_contract.rules.infrastructure import FileRepository
from agentic.features.workspace_contract.workspace_sync.domain import SharedRulePath, WorkspaceContractLayout
from agentic.features.workspace_contract.workspace_sync.infrastructure import PackagedRulesReader, WorkspaceReader, WorkspaceWriter


class WorkspaceContractInfrastructurePackageTests(unittest.TestCase):
    def test_workspace_sync_infrastructure_package_exports_expected_public_seam(self) -> None:
        self.assertEqual(
            workspace_sync_infrastructure.__all__,
            [
                "PackagedRulesReader",
                "WorkspaceReader",
                "WorkspaceWriter",
            ],
        )

    def test_rules_infrastructure_package_exports_expected_public_seam(self) -> None:
        self.assertEqual(
            rules_infrastructure.__all__,
            [
                "FileRepository",
                "file_repository",
            ],
        )

    def test_filesystem_anchor_exports_expected_public_seam(self) -> None:
        self.assertEqual(
            workspace_sync_infrastructure_filesystem.__all__,
            [
                "WorkspaceReader",
                "WorkspaceWriter",
            ],
        )
    def test_resources_anchor_exports_expected_public_seam(self) -> None:
        self.assertEqual(
            workspace_sync_infrastructure_resources.__all__,
            ["PackagedRulesReader"],
        )

    def test_infrastructure_directory_matches_allowed_anchor_shape(self) -> None:
        infrastructure_dir = Path(
            workspace_sync_infrastructure.__file__).resolve().parent
        entries = {
            path.name
            for path in infrastructure_dir.iterdir()
            if path.name != "__pycache__"
        }

        self.assertEqual(entries, {"__init__.py", "filesystem", "resources"})

        rules_infrastructure_dir = Path(
            rules_infrastructure.__file__).resolve().parent
        rules_entries = {
            path.name
            for path in rules_infrastructure_dir.iterdir()
            if path.name != "__pycache__"
        }

        self.assertEqual(rules_entries, {"__init__.py", "file_repository.py"})


class PackagedRulesReaderTests(unittest.TestCase):
    _forbidden_rule_stack_terms = {
        r"\btypescript\b": "typescript",
        r"\bjavascript\b": "javascript",
        r"\bphp\b": "php",
        r"\bjava\b": "java",
        r"\bruby\b": "ruby",
        r"\brust\b": "rust",
        r"\bkotlin\b": "kotlin",
        r"\bswift\b": "swift",
        r"\bscala\b": "scala",
        r"\belixir\b": "elixir",
        r"\bclojure\b": "clojure",
        r"\bdjango\b": "django",
        r"\bflask\b": "flask",
        r"\bfastapi\b": "fastapi",
        r"\breact\b": "react",
        r"\bvue\b": "vue",
        r"\bangular\b": "angular",
        r"\bsvelte\b": "svelte",
        r"\bnext\.js\b": "next.js",
        r"\bnuxt\b": "nuxt",
        r"\bnestjs\b": "nestjs",
        r"\blaravel\b": "laravel",
        r"\bsymfony\b": "symfony",
        r"\brails\b": "rails",
        r"\basp\.net\b": "asp.net",
        r"\bdotnet\b": "dotnet",
        r"\bnpm\b": "npm",
        r"\bpnpm\b": "pnpm",
        r"\byarn\b": "yarn",
        r"\bpip\b": "pip",
        r"\bpoetry\b": "poetry",
        r"\bcomposer\b": "composer",
        r"\bmaven\b": "maven",
        r"\bgradle\b": "gradle",
        r"\bclick\b": "click",
        r"\bdocker\b": "docker",
        r"\bkubernetes\b": "kubernetes",
        r"\bterraform\b": "terraform",
        r"\bansible\b": "ansible",
        r"\bsubprocess(?:es)?\b": "subprocess",
        r"\bfilesystem\b": "filesystem",
        r"\bnetwork\b": "network",
        r"\bendpoint(?:s)?\b": "endpoint",
    }

    def test_iter_shared_rule_paths_reads_packaged_rules_tree(self) -> None:
        reader = PackagedRulesReader()

        shared_rule_paths = reader.iter_shared_rule_paths()
        rendered_paths = tuple(path.as_posix() for path in shared_rule_paths)

        self.assertIn("INDEX.md", rendered_paths)
        self.assertIn("structure/INDEX.md", rendered_paths)
        self.assertIn("structure/feature/layers/FILE_TREE.md", rendered_paths)
        self.assertIn("project/structure/feature/layers/LAYERS.md", rendered_paths)
        self.assertIn("architecture/BOUNDARIES.md", rendered_paths)
        self.assertIn("execution/STEP.md", rendered_paths)
        self.assertEqual(rendered_paths, tuple(sorted(rendered_paths)))

    def test_reads_packaged_rule_text_and_default_config(self) -> None:
        reader = PackagedRulesReader()

        self.assertIn("# Rules", reader.read_document_text(
            SharedRulePath(Path("INDEX.md"))))
        self.assertIn("language:", reader.default_config_text())

    def test_iter_rule_document_paths_returns_relative_paths(self) -> None:
        reader = PackagedRulesReader()

        document_paths = reader.iter_rule_document_paths()

        self.assertIn(Path("INDEX.md"), document_paths)
        self.assertIn(Path("structure") / "MODULE.md", document_paths)
        self.assertIn(Path("structure") / "feature" / "layers" /
                  "LAYERS.md", document_paths)
        self.assertIn(Path("project") / "structure" / "feature" / "layers" /
                  "FILE_TREE.md", document_paths)
        self.assertIn(Path("execution") / "BIG_PICTURE.md", document_paths)
        self.assertFalse(any(path.is_absolute() for path in document_paths))

    def test_read_rule_document_text_accepts_relative_path(self) -> None:
        reader = PackagedRulesReader()

        document_text = reader.read_rule_document_text(Path("INDEX.md"))

        self.assertIn("## Stop Or Descend", document_text)

    def test_reads_managed_bootstrap_instruction_text(self) -> None:
        reader = PackagedRulesReader()

        self.assertEqual(
            reader.default_bootstrap_instruction_text(),
            "# agentic\n\nGo to the `agentic/` folder and explore it. You will find the project guidance there.\n",
        )

    def test_resources_guide_embeds_exact_bootstrap_instruction_text(self) -> None:
        reader = PackagedRulesReader()
        resources_guide = Path(__file__).resolve(
        ).parents[1] / "src" / "agentic" / "resources" / "README.md"
        expected_block = f"```md\n{reader.default_bootstrap_instruction_text().rstrip()}\n```"

        self.assertIn(expected_block,
                      resources_guide.read_text(encoding="utf-8"))

    def test_packaged_rule_docs_remain_tech_stack_agnostic(self) -> None:
        reader = PackagedRulesReader()
        findings: list[str] = []

        for document_path in reader.iter_rule_document_paths():
            document_text = reader.read_rule_document_text(
                document_path).lower()
            for pattern, label in self._forbidden_rule_stack_terms.items():
                if re.search(pattern, document_text) is not None:
                    findings.append(f"{document_path.as_posix()}: {label}")

        self.assertEqual(findings, [])


class WorkspaceFilesystemAdapterTests(unittest.TestCase):
    def test_writer_creates_target_directory(self) -> None:
        writer = WorkspaceWriter()
        layout = WorkspaceContractLayout()

        with TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)

            target_dir, created_dir = writer.ensure_target_directory(
                project_root, layout=layout)

            self.assertTrue(created_dir)
            self.assertEqual(target_dir, project_root / "agentic")

    def test_reader_reports_existing_workspace_paths(self) -> None:
        reader = WorkspaceReader()
        writer = WorkspaceWriter()
        layout = WorkspaceContractLayout()

        with TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            writer.ensure_target_directory(project_root, layout=layout)

            agent_document = layout.shared_rule_destination(
                project_root, SharedRulePath(Path("INDEX.md")))
            writer.write_text(agent_document, "agent rules\n")
            writer.write_text(layout.config_path(
                project_root), "language: python\n")
            writer.write_text(
                layout.bootstrap_instruction_path(project_root),
                "# agentic\n\nGo to agentic\n",
            )
            self.assertTrue(reader.agentic_dir_exists(
                project_root, layout=layout))
            self.assertTrue(reader.config_exists(project_root, layout=layout))
            self.assertTrue(reader.path_exists(
                layout.bootstrap_instruction_path(project_root)))
            self.assertEqual(
                reader.existing_shared_rule_paths(
                    project_root,
                    [SharedRulePath(Path("structure") / "MODULE.md"),
                     SharedRulePath(Path("INDEX.md"))],
                    layout=layout,
                ),
                (project_root / "agentic" / "rules" / "INDEX.md",),
            )
            self.assertEqual(reader.read_text(agent_document), "agent rules\n")
            self.assertEqual(reader.list_override_paths(
                project_root, layout=layout), ())
            self.assertEqual(reader.list_project_specific_paths(
                project_root, layout=layout), ())

    def test_reader_lists_only_managed_rule_documents(self) -> None:
        reader = WorkspaceReader()
        writer = WorkspaceWriter()
        layout = WorkspaceContractLayout()

        with TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            writer.ensure_target_directory(project_root, layout=layout)

            managed_rule = layout.rules_dir(project_root) / "INDEX.md"
            nested_managed_rule = layout.rules_dir(
                project_root) / "structure" / "FEATURE.md"
            nested_managed_rule.parent.mkdir(parents=True, exist_ok=True)
            hidden_rule = layout.rules_dir(
                project_root) / ".cache" / "IGNORED.md"
            hidden_rule.parent.mkdir(parents=True, exist_ok=True)

            writer.write_text(managed_rule, "# Rules\n")
            writer.write_text(nested_managed_rule, "# Feature Rules\n")
            writer.write_text(hidden_rule, "# Hidden\n")

            self.assertEqual(
                reader.existing_rule_document_paths(
                    project_root, layout=layout),
                (managed_rule, nested_managed_rule),
            )

    def test_writer_rejects_file_in_place_of_target_directory(self) -> None:
        writer = WorkspaceWriter()

        with TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            (project_root / "agentic").write_text("not a directory\n", encoding="utf-8")

            with self.assertRaises(NotADirectoryError):
                writer.ensure_target_directory(project_root)
class FileRepositoryTests(unittest.TestCase):
    def test_find_returns_refactored_rule_documents(self) -> None:
        documents = FileRepository().find()

        paths = {document.path.as_posix() for document in documents}

        self.assertIn("INDEX.md", paths)
        self.assertIn("architecture/BOUNDARIES.md", paths)
        self.assertIn("execution/STEP.md", paths)
        self.assertIn("project/structure/feature/layers/LAYERS.md", paths)


if __name__ == "__main__":
    unittest.main()
