from __future__ import annotations

from collections.abc import Iterable
from importlib.resources import files
from pathlib import Path

from ..domain.sync_policy import CONFIG_FILE_NAME, CORE_RULE_DOCUMENTS
from ..ports import ResourceDocument


class PackagedWorkspaceResources:
    def iter_shared_documents(self) -> Iterable[ResourceDocument]:
        rules_root = files("agentic").joinpath("resources", "rules")
        for document_name in CORE_RULE_DOCUMENTS:
            yield ResourceDocument(
                relative_path=Path("rules") / document_name,
                text=rules_root.joinpath(
                    document_name).read_text(encoding="utf-8"),
            )

    def default_config_text(self) -> str:
        return files("agentic").joinpath("resources", CONFIG_FILE_NAME).read_text(encoding="utf-8")
