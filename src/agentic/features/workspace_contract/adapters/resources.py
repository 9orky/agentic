from __future__ import annotations

from collections.abc import Iterable
from importlib.resources import files
from pathlib import Path

from ..domain.sync_policy import CONFIG_FILE_NAME, SHARED_RULE_PATHS
from ..ports import ResourceDocument


class PackagedWorkspaceResources:
    def iter_shared_documents(self) -> Iterable[ResourceDocument]:
        rules_root = files("agentic").joinpath("resources", "rules")
        for rule_path in SHARED_RULE_PATHS:
            yield ResourceDocument(
                relative_path=Path("rules") / rule_path,
                text=rules_root.joinpath(*rule_path.parts).read_text(
                    encoding="utf-8"),
            )

    def default_config_text(self) -> str:
        return files("agentic").joinpath("resources", CONFIG_FILE_NAME).read_text(encoding="utf-8")
