import re
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from agentic.features.workspace_contract.contract.domain import RuleDocumentClass, SharedRulePath, WorkspaceContractLayout
from agentic.features.workspace_contract.contract.infrastructure import PackagedRulesReader, RuleMarkdownParser, RuleTreeReader, WorkspaceReader, WorkspaceWriter


class PackagedRulesReaderTests(unittest.TestCase):
    _forbidden_rule_stack_terms = {
        r"\bpython\b": "python",
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
        r"\bcli\b": "cli",
        r"\bendpoint(?:s)?\b": "endpoint",
    }

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

    def test_iter_rule_document_paths_returns_relative_paths(self) -> None:
        reader = PackagedRulesReader()

        document_paths = reader.iter_rule_document_paths()

        self.assertIn(Path("AGENT.md"), document_paths)
        self.assertIn(Path("planning") / "PLANNING.md", document_paths)
        self.assertFalse(any(path.is_absolute() for path in document_paths))

    def test_read_rule_document_text_accepts_relative_path(self) -> None:
        reader = PackagedRulesReader()

        document_text = reader.read_rule_document_text(Path("AGENT.md"))

        self.assertIn("## Navigation Rule", document_text)

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
            writer.write_text(
                layout.bootstrap_instruction_path(project_root),
                "# agentic\n\nGo to agentic\n",
            )
            override_path = layout.overrides_dir(project_root) / "TESTS.md"
            project_specific_path = layout.project_specific_dir(
                project_root) / "LOCAL.md"
            writer.write_text(override_path, "override\n")
            writer.write_text(project_specific_path, "local\n")

            self.assertTrue(reader.agentic_dir_exists(
                project_root, layout=layout))
            self.assertTrue(reader.config_exists(project_root, layout=layout))
            self.assertTrue(reader.path_exists(
                layout.bootstrap_instruction_path(project_root)))
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

    def test_reader_lists_only_managed_rule_documents(self) -> None:
        reader = WorkspaceReader()
        writer = WorkspaceWriter()
        layout = WorkspaceContractLayout()

        with TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            writer.ensure_target_directory(project_root, layout=layout)
            writer.ensure_local_extension_directories(
                project_root, layout=layout)

            managed_rule = layout.rules_dir(project_root) / "AGENT.md"
            nested_managed_rule = layout.rules_dir(
                project_root) / "feature" / "FEATURE.md"
            nested_managed_rule.parent.mkdir(parents=True, exist_ok=True)
            override_rule = layout.overrides_dir(project_root) / "LOCAL.md"
            hidden_rule = layout.rules_dir(
                project_root) / ".cache" / "IGNORED.md"
            hidden_rule.parent.mkdir(parents=True, exist_ok=True)

            writer.write_text(managed_rule, "# Agent Rules\n")
            writer.write_text(nested_managed_rule, "# Feature Rules\n")
            writer.write_text(override_rule, "# Override\n")
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


class RuleTreeReaderTests(unittest.TestCase):
    def test_iter_packaged_rule_documents_returns_sorted_relative_paths(self) -> None:
        reader = RuleTreeReader()

        document_paths = reader.iter_packaged_rule_documents()

        self.assertIn(Path("AGENT.md"), document_paths)
        self.assertIn(Path("feature") / "module" /
                      "layers" / "DOMAIN.md", document_paths)
        self.assertEqual(document_paths, tuple(
            sorted(document_paths, key=lambda path: path.as_posix())))

    def test_iter_local_rule_documents_returns_managed_local_files(self) -> None:
        reader = RuleTreeReader()
        writer = WorkspaceWriter()
        layout = WorkspaceContractLayout()

        with TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            writer.ensure_target_directory(project_root, layout=layout)
            writer.ensure_local_extension_directories(
                project_root, layout=layout)
            managed_rule = layout.rules_dir(project_root) / "AGENT.md"
            writer.write_text(managed_rule, "# Agent Rules\n")

            self.assertEqual(reader.iter_local_rule_documents(
                project_root), (managed_rule,))


class RuleMarkdownParserTests(unittest.TestCase):
    def test_parses_headings_and_navigation_targets(self) -> None:
        parser = RuleMarkdownParser()

        document = parser.parse(
            """# Agent Rules

## Available Options

### Child Paths

See [Feature](feature/FEATURE.md) and [Planning](planning/PLANNING.md).

## Navigation Rule

1. Follow one link.
""",
            source_path=Path("AGENT.md"),
        )

        self.assertEqual(document.headings,
                         ("Available Options", "Child Paths", "Navigation Rule"))
        self.assertEqual(document.section_headings,
                         ("Available Options", "Navigation Rule"))
        self.assertEqual(document.anchor_headings, ("Child Paths",))
        self.assertEqual(document.navigation_targets,
                         ("feature/FEATURE.md", "planning/PLANNING.md"))
        self.assertTrue(document.has_navigation_targets)
        self.assertEqual(document.document_class,
                         RuleDocumentClass.NAVIGATIONAL)

    def test_reads_document_class_from_frontmatter(self) -> None:
        parser = RuleMarkdownParser()

        document = parser.parse(
            """---
document_class: leaf
---
# Tests Rules

## Core Rules

1. Test behavior.
""",
            source_path=Path("tests/TESTS.md"),
        )

        self.assertEqual(document.declared_document_class,
                         RuleDocumentClass.LEAF)
        self.assertEqual(document.document_class, RuleDocumentClass.LEAF)

    def test_reads_document_class_from_inline_marker(self) -> None:
        parser = RuleMarkdownParser()

        document = parser.parse(
            """# Planning Rules

Document Class: navigational

## Planning Options

1. Use the plan.
""",
            source_path=Path("planning/PLANNING.md"),
        )

        self.assertEqual(document.declared_document_class,
                         RuleDocumentClass.NAVIGATIONAL)
        self.assertEqual(document.document_class,
                         RuleDocumentClass.NAVIGATIONAL)

    def test_defaults_to_leaf_when_navigation_hints_are_absent(self) -> None:
        parser = RuleMarkdownParser()

        document = parser.parse(
            """# Domain Layer Rules

## Ownership

1. Domain owns entities.

## Acceptance Check

1. The model is valid.
""",
            source_path=Path("feature/module/layers/DOMAIN.md"),
        )

        self.assertIsNone(document.declared_document_class)
        self.assertEqual(document.document_class, RuleDocumentClass.LEAF)


if __name__ == "__main__":
    unittest.main()
