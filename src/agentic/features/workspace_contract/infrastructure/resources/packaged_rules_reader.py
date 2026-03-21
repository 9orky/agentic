from __future__ import annotations

from collections.abc import Iterable
from importlib.resources import files
from pathlib import Path

from ...domain import SharedRulePath


class PackagedRulesReader:
    def iter_shared_rule_paths(self) -> tuple[SharedRulePath, ...]:
        rules_root = files("agentic").joinpath("resources", "rules")
        return tuple(self._iter_shared_rule_paths(rules_root, Path()))

    def read_document_text(self, shared_rule_path: SharedRulePath) -> str:
        rules_root = files("agentic").joinpath("resources", "rules")
        return rules_root.joinpath(*shared_rule_path.relative_path.parts).read_text(encoding="utf-8")

    def default_config_text(self) -> str:
        return files("agentic").joinpath("resources", "agentic.yaml").read_text(encoding="utf-8")

    def default_bootstrap_instruction_text(self) -> str:
        return files("agentic").joinpath("resources", "copilot-instructions.md").read_text(encoding="utf-8")

    def _iter_shared_rule_paths(self, directory, relative_path: Path) -> Iterable[SharedRulePath]:
        for child in sorted(directory.iterdir(), key=lambda item: item.name):
            child_relative_path = relative_path / child.name
            if child.is_dir():
                if child.name in {"overrides", "project-specific"}:
                    continue
                yield from self._iter_shared_rule_paths(child, child_relative_path)
                continue

            if child.name.startswith("."):
                continue
            if child_relative_path.suffix != ".md":
                continue

            yield SharedRulePath(child_relative_path)
