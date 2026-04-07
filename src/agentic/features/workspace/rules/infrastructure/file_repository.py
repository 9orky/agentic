from __future__ import annotations

from collections.abc import Iterable
from importlib.resources import files
from pathlib import Path

from pydantic import TypeAdapter

from ..domain import RuleDocumentFile, RuleDocumentRepository


class FileRepository(RuleDocumentRepository):
    def __init__(self) -> None:
        self._document_adapter = TypeAdapter(RuleDocumentFile)

    def find(self) -> tuple[RuleDocumentFile, ...]:
        rules_root = files("agentic").joinpath("resources", "rules")
        return tuple(self._iter_documents(rules_root, Path()))

    def _iter_documents(self, directory, relative_path: Path) -> Iterable[RuleDocumentFile]:
        for child in sorted(directory.iterdir(), key=lambda item: item.name):
            child_relative_path = relative_path / child.name
            if child.is_dir():
                yield from self._iter_documents(child, child_relative_path)
                continue

            if child.name.startswith("."):
                continue
            if child_relative_path.suffix != ".md":
                continue

            yield self._document_adapter.validate_python(
                {
                    "path": child_relative_path,
                    "content": child.read_text(encoding="utf-8"),
                }
            )


__all__ = ["FileRepository"]
