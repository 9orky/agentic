from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
import os
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from agentic.cli import main
from agentic.features.workspace_contract import bootstrap_project


class CliTests(unittest.TestCase):
    def test_help_command_prints_command_summary(self) -> None:
        output = StringIO()

        with redirect_stdout(output):
            exit_code = main(["help"])

        self.assertEqual(exit_code, 0)
        rendered = output.getvalue()
        self.assertIn("usage:", rendered.lower())
        self.assertIn("Bootstrap a project's agentic surface", rendered)
        self.assertIn("check", rendered)
        self.assertIn("init", rendered)
        self.assertIn("help", rendered)
        self.assertIn("llm", rendered)
        self.assertIn("update", rendered)
        self.assertNotIn("--llm", rendered)

    def test_update_command_refreshes_shared_docs(self) -> None:
        with TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)

            main(["init", "--project-root", str(project_root)])
            shared_doc_path = project_root / "agentic" / "rules" / "AGENT.md"
            shared_doc_path.write_text(
                "locally modified shared doc\n", encoding="utf-8")

            output = StringIO()
            with redirect_stdout(output):
                exit_code = main(
                    ["update", "--project-root", str(project_root)])

            self.assertEqual(exit_code, 0)
            self.assertIn("Updated", output.getvalue())
            self.assertIn("agentic llm update", output.getvalue())
            self.assertIn("agentic check", output.getvalue())
            self.assertNotEqual(shared_doc_path.read_text(
                encoding="utf-8"), "locally modified shared doc\n")

    def test_check_command_prints_summary_before_pass_message(self) -> None:
        with TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            (project_root / "src" / "domain").mkdir(parents=True)
            (project_root / "src" / "generated").mkdir(parents=True)
            (project_root / "agentic").mkdir()

            (project_root / "src" / "domain" / "logic.py").write_text(
                "from src.domain.helpers import helper\n",
                encoding="utf-8",
            )
            (project_root / "src" / "generated" / "client.py").write_text(
                "from src.domain.logic import Logic\n",
                encoding="utf-8",
            )
            (project_root / "agentic" / "agentic.yaml").write_text(
                "language: python\n"
                "exclusions:\n"
                "  - src/generated\n"
                "rules:\n"
                "  boundaries:\n"
                "    - source: src/domain\n"
                "      disallow:\n"
                "        - src/infra\n",
                encoding="utf-8",
            )

            output = StringIO()
            with redirect_stdout(output):
                exit_code = main(
                    ["check", "--project-root", str(project_root)])

            self.assertEqual(exit_code, 0)
            rendered = output.getvalue()
            self.assertTrue(rendered.startswith("Check Summary:\n"))
            self.assertIn("- Files found in scope: 2", rendered)
            self.assertIn("- Files excluded by rules: 1", rendered)
            self.assertIn("- Files checked: 1", rendered)
            self.assertIn(
                "Architecture Check Passed! No violations found.", rendered)

    def test_check_command_prints_summary_before_violations(self) -> None:
        with TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            (project_root / "src" / "domain").mkdir(parents=True)
            (project_root / "src" / "infra").mkdir(parents=True)
            (project_root / "agentic").mkdir()

            (project_root / "src" / "infra" / "database.py").write_text(
                "class Database:\n    pass\n",
                encoding="utf-8",
            )
            (project_root / "src" / "domain" / "logic.py").write_text(
                "from src.infra.database import Database\n",
                encoding="utf-8",
            )
            (project_root / "agentic" / "agentic.yaml").write_text(
                "language: python\n"
                "rules:\n"
                "  boundaries:\n"
                "    - source: src/domain\n"
                "      disallow:\n"
                "        - src/infra\n",
                encoding="utf-8",
            )

            output = StringIO()
            with redirect_stdout(output):
                exit_code = main(
                    ["check", "--project-root", str(project_root)])

            self.assertEqual(exit_code, 1)
            rendered = output.getvalue()
            self.assertTrue(rendered.startswith("Check Summary:\n"))
            self.assertIn("- Files found in scope: 2", rendered)
            self.assertIn("- Files excluded by rules: 0", rendered)
            self.assertIn("- Files checked: 2", rendered)
            self.assertIn(
                "=== Architectural Violations Detected ===", rendered)

    def test_root_invocation_bootstraps_current_directory(self) -> None:
        with TemporaryDirectory() as temp_dir:
            previous_cwd = Path.cwd()
            output = StringIO()
            try:
                os.chdir(temp_dir)
                with redirect_stdout(output):
                    exit_code = main([])
            finally:
                os.chdir(previous_cwd)

            self.assertEqual(exit_code, 0)
            self.assertTrue(
                (Path(temp_dir) / "agentic" / "agentic.yaml").exists())
            self.assertIn("Created", output.getvalue())
            self.assertIn(
                "Safe to rerun: plain 'agentic' preserves existing local files.", output.getvalue())
            self.assertIn("Next step: run 'agentic llm'", output.getvalue())

    def test_llm_command_bootstraps_and_prints_prompt(self) -> None:
        with TemporaryDirectory() as temp_dir:
            previous_cwd = Path.cwd()
            output = StringIO()
            try:
                os.chdir(temp_dir)
                with redirect_stdout(output):
                    exit_code = main(["llm"])
            finally:
                os.chdir(previous_cwd)

            self.assertEqual(exit_code, 0)
            self.assertTrue(
                (Path(temp_dir) / "agentic" / "agentic.yaml").exists())
            rendered = output.getvalue()
            self.assertIn(
                "You are the downstream LLM for a project that uses agentic.", rendered)
            self.assertIn("agentic llm bootstrap", rendered)
            self.assertIn("agentic llm architecture", rendered)
            self.assertIn("first-configuration interview", rendered)
            self.assertIn("concise chat summary", rendered)
            self.assertNotIn("agentic/rules/AGENT.md", rendered)

    def test_llm_anchor_command_prints_placeholder_contract(self) -> None:
        with TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            bootstrap_project(project_root)
            config_path = project_root / "agentic" / "agentic.yaml"
            config_path.write_text(
                "language: python\n"
                "exclusions:\n"
                "  - tests/**\n"
                "rules:\n"
                "  boundaries:\n"
                "    - source: src/domain\n"
                "      disallow:\n"
                "        - src/infra\n",
                encoding="utf-8",
            )
            output = StringIO()

            with redirect_stdout(output):
                exit_code = main(
                    ["llm", "--project-root", str(project_root), "config"])

            self.assertEqual(exit_code, 0)
            rendered = output.getvalue()
            self.assertIn("Anchor: config", rendered)
            self.assertIn("Command: agentic llm config", rendered)
            self.assertIn("Language: python", rendered)
            self.assertIn("Exclusion patterns: 1", rendered)
            self.assertIn("Boundary rules: 1", rendered)
            self.assertIn("source=src/domain", rendered)

    def test_llm_bootstrap_anchor_is_read_only_and_reports_missing_state(self) -> None:
        with TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            output = StringIO()

            with redirect_stdout(output):
                exit_code = main(
                    ["llm", "--project-root", str(project_root), "bootstrap"])

            self.assertEqual(exit_code, 0)
            self.assertFalse((project_root / "agentic").exists())
            rendered = output.getvalue()
            self.assertIn("Anchor: bootstrap", rendered)
            self.assertIn("Local agentic directory: missing", rendered)
            self.assertIn("Plain `agentic` is safe to rerun", rendered)

    def test_llm_rules_anchor_reports_local_extension_files(self) -> None:
        with TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            bootstrap_project(project_root)

            override_path = project_root / "agentic" / "rules" / "overrides" / "FEATURE.md"
            project_specific_path = project_root / "agentic" / \
                "rules" / "project-specific" / "TEAM_BOUNDARIES.md"
            override_path.write_text("local override\n", encoding="utf-8")
            project_specific_path.write_text("local rule\n", encoding="utf-8")

            output = StringIO()
            with redirect_stdout(output):
                exit_code = main(
                    ["llm", "--project-root", str(project_root), "rules"])

            self.assertEqual(exit_code, 0)
            rendered = output.getvalue()
            self.assertIn("Anchor: rules", rendered)
            self.assertIn("Local override files: 1", rendered)
            self.assertIn("Local project-specific rule files: 1", rendered)
            self.assertIn("agentic/rules/overrides/FEATURE.md", rendered)
            self.assertIn(
                "agentic/rules/project-specific/TEAM_BOUNDARIES.md", rendered)

    def test_llm_update_anchor_reports_missing_shared_docs(self) -> None:
        with TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            bootstrap_project(project_root)

            missing_shared_doc = project_root / "agentic" / "rules" / "AGENT.md"
            missing_shared_doc.unlink()

            output = StringIO()
            with redirect_stdout(output):
                exit_code = main(
                    ["llm", "--project-root", str(project_root), "update"])

            self.assertEqual(exit_code, 0)
            self.assertFalse(missing_shared_doc.exists())
            rendered = output.getvalue()
            self.assertIn("Anchor: update", rendered)
            self.assertIn("Shared docs that update would restore", rendered)
            self.assertIn("agentic/rules/AGENT.md", rendered)
            self.assertIn("Run `agentic update`", rendered)

    def test_llm_config_anchor_requeries_current_config_after_changes(self) -> None:
        with TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            bootstrap_project(project_root)
            config_path = project_root / "agentic" / "agentic.yaml"

            config_path.write_text(
                "language: python\n"
                "rules:\n"
                "  boundaries:\n"
                "    - source: src/domain\n"
                "      disallow:\n"
                "        - src/infra\n",
                encoding="utf-8",
            )

            first_output = StringIO()
            with redirect_stdout(first_output):
                first_exit_code = main(
                    ["llm", "--project-root", str(project_root), "config"])

            config_path.write_text(
                "language: php\n"
                "exclusions:\n"
                "  - vendor/**\n"
                "rules:\n"
                "  boundaries:\n"
                "    - source: src/app\n"
                "      disallow:\n"
                "        - src/legacy\n"
                "      allow:\n"
                "        - src/app/public\n",
                encoding="utf-8",
            )

            second_output = StringIO()
            with redirect_stdout(second_output):
                second_exit_code = main(
                    ["llm", "--project-root", str(project_root), "config"])

            self.assertEqual(first_exit_code, 0)
            self.assertEqual(second_exit_code, 0)
            self.assertIn("Language: python", first_output.getvalue())
            self.assertIn("Language: php", second_output.getvalue())
            self.assertIn("Exclusions: vendor/**", second_output.getvalue())
            self.assertIn("source=src/app", second_output.getvalue())

    def test_llm_architecture_anchor_reports_current_validation_facts(self) -> None:
        with TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            (project_root / "src" / "domain").mkdir(parents=True)
            (project_root / "src" / "infra").mkdir(parents=True)
            (project_root / "agentic").mkdir()

            (project_root / "src" / "infra" / "database.py").write_text(
                "class Database:\n    pass\n",
                encoding="utf-8",
            )
            (project_root / "src" / "domain" / "logic.py").write_text(
                "from src.infra.database import Database\n",
                encoding="utf-8",
            )
            (project_root / "agentic" / "agentic.yaml").write_text(
                "language: python\n"
                "rules:\n"
                "  boundaries:\n"
                "    - source: src/domain\n"
                "      disallow:\n"
                "        - src/infra\n",
                encoding="utf-8",
            )

            output = StringIO()
            with redirect_stdout(output):
                exit_code = main(
                    ["llm", "--project-root", str(project_root), "architecture"])

            self.assertEqual(exit_code, 0)
            rendered = output.getvalue()
            self.assertIn("Anchor: architecture", rendered)
            self.assertIn("Language: python", rendered)
            self.assertIn("Required extractor runtime:", rendered)
            self.assertIn("Files found in scope: 2", rendered)
            self.assertIn("Current boundary violations: 1", rendered)
            self.assertIn("src/domain/logic.py", rendered)
            self.assertIn("Run `agentic check`", rendered)

    def test_llm_architecture_anchor_requeries_after_config_changes(self) -> None:
        with TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            (project_root / "src" / "domain").mkdir(parents=True)
            (project_root / "src" / "generated").mkdir(parents=True)
            (project_root / "agentic").mkdir()

            (project_root / "src" / "domain" / "logic.py").write_text(
                "from src.domain.helpers import helper\n",
                encoding="utf-8",
            )
            (project_root / "src" / "generated" / "client.py").write_text(
                "from src.domain.logic import Logic\n",
                encoding="utf-8",
            )
            config_path = project_root / "agentic" / "agentic.yaml"
            config_path.write_text(
                "language: python\n"
                "rules:\n"
                "  boundaries:\n"
                "    - source: src/domain\n"
                "      disallow:\n"
                "        - src/infra\n",
                encoding="utf-8",
            )

            first_output = StringIO()
            with redirect_stdout(first_output):
                first_exit_code = main(
                    ["llm", "--project-root", str(project_root), "architecture"])

            config_path.write_text(
                "language: python\n"
                "exclusions:\n"
                "  - src/generated\n"
                "rules:\n"
                "  boundaries:\n"
                "    - source: src/domain\n"
                "      disallow:\n"
                "        - src/infra\n",
                encoding="utf-8",
            )

            second_output = StringIO()
            with redirect_stdout(second_output):
                second_exit_code = main(
                    ["llm", "--project-root", str(project_root), "architecture"])

            self.assertEqual(first_exit_code, 0)
            self.assertEqual(second_exit_code, 0)
            self.assertIn("Files excluded by rules: 0",
                          first_output.getvalue())
            self.assertIn("Files checked: 2", first_output.getvalue())
            self.assertIn("Files excluded by rules: 1",
                          second_output.getvalue())
            self.assertIn("Files checked: 1", second_output.getvalue())

    def test_llm_flag_is_not_supported(self) -> None:
        stdout = StringIO()
        stderr = StringIO()

        with redirect_stdout(stdout), redirect_stderr(stderr):
            exit_code = main(["--llm"])

        self.assertEqual(exit_code, 2)
        self.assertIn("No such option: --llm", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
