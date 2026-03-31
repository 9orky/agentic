from __future__ import annotations

from collections.abc import Iterable
from importlib.resources import files
from pathlib import Path

from ..domain import SharedRuleDocument, SharedRulePath, Workspace, WorkspaceContractLayout, WorkspaceRepository


class FileRepository(WorkspaceRepository):
    def load(self, path: Path) -> Workspace:
        project_root = Path(path).resolve()
        layout = WorkspaceContractLayout()
        shared_rule_documents = self._load_shared_rule_documents()

        return Workspace(
            project_root=project_root,
            shared_rule_documents=shared_rule_documents,
            config_content=self._packaged_config_content(),
            bootstrap_instruction_content=self._packaged_bootstrap_instruction_content(),
            existing_shared_rule_paths=self._existing_shared_rule_paths(
                project_root,
                layout,
                shared_rule_documents,
            ),
            override_paths=self._list_workspace_files(
                layout.overrides_dir(project_root)),
            project_specific_paths=self._list_workspace_files(
                layout.project_specific_dir(project_root)),
            agentic_dir_exists=layout.target_dir(project_root).is_dir(),
            config_exists=layout.config_path(project_root).is_file(),
            bootstrap_instruction_exists=layout.bootstrap_instruction_path(
                project_root).is_file(),
            layout=layout,
        )

    def _load_shared_rule_documents(self) -> tuple[SharedRuleDocument, ...]:
        rules_root = files("agentic").joinpath("resources", "rules")
        return tuple(self._iter_shared_rule_documents(rules_root, Path()))

    def _iter_shared_rule_documents(self, directory, relative_path: Path) -> Iterable[SharedRuleDocument]:
        for child in sorted(directory.iterdir(), key=lambda item: item.name):
            if child.name.startswith("."):
                continue

            child_relative_path = relative_path / child.name
            if child.is_dir():
                yield from self._iter_shared_rule_documents(child, child_relative_path)
                continue

            if child_relative_path.suffix != ".md":
                continue

            yield SharedRuleDocument(
                shared_rule_path=SharedRulePath(child_relative_path),
                content=child.read_text(encoding="utf-8"),
            )

    def _existing_shared_rule_paths(
        self,
        project_root: Path,
        layout: WorkspaceContractLayout,
        shared_rule_documents: tuple[SharedRuleDocument, ...],
    ) -> tuple[Path, ...]:
        return tuple(
            target_path
            for target_path in (
                layout.shared_rule_destination(
                    project_root, document.shared_rule_path)
                for document in shared_rule_documents
            )
            if target_path.is_file()
        )

    def _list_workspace_files(self, root: Path) -> tuple[Path, ...]:
        if not root.is_dir():
            return ()

        return tuple(self._iter_workspace_files(root))

    def _iter_workspace_files(self, directory: Path) -> Iterable[Path]:
        for child in sorted(directory.iterdir(), key=lambda item: item.name):
            if child.name.startswith("."):
                continue
            if child.is_dir():
                yield from self._iter_workspace_files(child)
                continue
            yield child

    def _packaged_config_content(self) -> str:
        return files("agentic").joinpath("resources", "agentic.yaml").read_text(encoding="utf-8")

    def _packaged_bootstrap_instruction_content(self) -> str:
        return files("agentic").joinpath("resources", "copilot-instructions.md").read_text(encoding="utf-8")


__all__ = ["FileRepository"]
