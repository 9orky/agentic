from __future__ import annotations

import os
import tempfile
import unittest

from click.testing import CliRunner

from agentic.cli import agentic_cli


class RuleSchemaCliTests(unittest.TestCase):
    def setUp(self) -> None:
        self.runner = CliRunner()
        self._temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self._temp_dir.cleanup)
        self.cwd = self._temp_dir.name

    def test_check_rule_schema_command_renders_packaged_rule_coverage(self) -> None:
        result = self._invoke_from_cwd(["check-rule-schema"])

        self.assertEqual(result.exit_code, 0, result.output)
        self.assertIn("Documents discovered:", result.output)
        self.assertIn("Documents checked:", result.output)
        self.assertIn("Collection coverage: complete.", result.output)

    def _invoke_from_cwd(self, args: list[str]):
        previous_cwd = os.getcwd()
        try:
            os.chdir(self.cwd)
            return self.runner.invoke(agentic_cli, args, catch_exceptions=False)
        finally:
            os.chdir(previous_cwd)


if __name__ == "__main__":
    unittest.main()
