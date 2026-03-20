from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from agentic.features.llm_handoff import build_llm_prompt


class LlmHandoffTests(unittest.TestCase):
    def test_build_llm_prompt_mentions_local_agentic_contract(self) -> None:
        with TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)

            prompt = build_llm_prompt(project_root)

            self.assertIn("agentic/guide/WORKFLOW.md", prompt)
            self.assertIn("agentic/guide/COMMANDS.md", prompt)
            self.assertIn("agentic/agentic.yaml", prompt)
            self.assertIn("durable collaboration surface", prompt)


if __name__ == "__main__":
    unittest.main()
