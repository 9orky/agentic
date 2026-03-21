from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
import os
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from agentic.cli import main


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
            self.assertIn("review refreshed rules", output.getvalue())
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
            self.assertIn("review agentic/agentic.yaml", output.getvalue())

    def test_llm_flag_is_not_supported(self) -> None:
        stdout = StringIO()
        stderr = StringIO()

        with redirect_stdout(stdout), redirect_stderr(stderr):
            exit_code = main(["--llm"])

        self.assertEqual(exit_code, 2)
        self.assertIn("No such option: --llm", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
