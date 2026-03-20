from __future__ import annotations

from collections.abc import Iterable
from importlib.resources import files
from pathlib import Path

from ..domain.sync_policy import CONFIG_FILE_NAME, SHARED_RESOURCE_DIRECTORIES
from ..ports import ResourceDocument


class PackagedWorkspaceResources:
    def iter_shared_documents(self) -> Iterable[ResourceDocument]:
        resource_root = files("agentic").joinpath("resources")
        for directory_name in SHARED_RESOURCE_DIRECTORIES:
            yield from self._walk_directory(
                resource_root.joinpath(directory_name),
                prefix=Path(directory_name),
            )

    def default_config_text(self) -> str:
        return files("agentic").joinpath("resources", CONFIG_FILE_NAME).read_text(encoding="utf-8")

    def _walk_directory(self, node, *, prefix: Path) -> Iterable[ResourceDocument]:
        for child in node.iterdir():
            child_prefix = prefix / child.name
            if child.is_dir():
                yield from self._walk_directory(child, prefix=child_prefix)
                continue
            if child.is_file():
                yield ResourceDocument(
                    relative_path=child_prefix,
                    text=child.read_text(encoding="utf-8"),
                )
