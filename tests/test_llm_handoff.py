from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from agentic.features.llm_handoff import build_llm_prompt


class LlmHandoffTests(unittest.TestCase):
    def test_build_llm_prompt_is_anchor_driven_and_non_path_based(self) -> None:
        with TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)

            prompt = build_llm_prompt(project_root)

            self.assertIn("agentic llm", prompt)
            self.assertIn("agentic llm bootstrap", prompt)
            self.assertIn("agentic llm rules", prompt)
            self.assertIn("agentic llm config", prompt)
            self.assertIn("agentic llm architecture", prompt)
            self.assertIn("agentic llm update", prompt)
            self.assertIn("Core rules are mandatory shared rails", prompt)
            self.assertIn("first-configuration interview", prompt)
            self.assertIn("Extend rules together with the user", prompt)
            self.assertIn("agentic check", prompt)
            self.assertIn("agentic update", prompt)
            self.assertIn("concise chat summary", prompt)
            self.assertIn("Deterministic workflow checklist", prompt)
            self.assertIn(
                "At the start of every request, recover current agentic facts",
                prompt,
            )
            self.assertIn(
                "Ensure the local `agentic/` directory exists",
                prompt,
            )
            self.assertIn(
                "future sessions should start with `agentic llm`", prompt)
            self.assertNotIn("agentic --llm", prompt)
            self.assertNotIn("src/agentic/resources", prompt)
            self.assertNotIn("src/agentic/features", prompt)
            self.assertNotIn("agentic/rules/AGENT.md", prompt)


if __name__ == "__main__":
    unittest.main()
