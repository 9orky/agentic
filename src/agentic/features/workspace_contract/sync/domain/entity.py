from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .value_object import (
    SharedRuleDocument,
    SyncAction,
    SyncChange,
    WorkspaceContractLayout,
    WorkspaceContractSummary,
    WorkspaceWritePlan,
)


@dataclass(frozen=True)
class Workspace:
    project_root: Path
    shared_rule_documents: tuple[SharedRuleDocument, ...]
    config_content: str
    bootstrap_instruction_content: str
    existing_shared_rule_paths: tuple[Path, ...] = ()
    local_paths: tuple[Path, ...] = ()
    agentic_dir_exists: bool = False
    config_exists: bool = False
    bootstrap_instruction_exists: bool = False
    layout: WorkspaceContractLayout = WorkspaceContractLayout()

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "shared_rule_documents",
            _sort_shared_rule_documents(tuple(self.shared_rule_documents)),
        )
        object.__setattr__(
            self,
            "existing_shared_rule_paths",
            _unique_paths(tuple(self.existing_shared_rule_paths)),
        )
        object.__setattr__(
            self,
            "local_paths",
            _unique_paths(tuple(self.local_paths)),
        )

    def expected_shared_rule_paths(self) -> tuple[Path, ...]:
        return tuple(
            self.layout.shared_rule_destination(
                self.project_root, document.shared_rule_path)
            for document in self.shared_rule_documents
        )

    def plan_bootstrap(self) -> WorkspaceWritePlan:
        return self._build_write_plan(
            overwrite_shared_rule_documents=False,
            overwrite_bootstrap_instruction=False,
        )

    def plan_update(self) -> WorkspaceWritePlan:
        return self._build_write_plan(
            overwrite_shared_rule_documents=True,
            overwrite_bootstrap_instruction=True,
        )

    def summarize(self) -> WorkspaceContractSummary:
        expected_shared_rule_paths = self.expected_shared_rule_paths()
        existing_shared_rule_paths = set(self.existing_shared_rule_paths)
        present_shared_rule_paths = tuple(
            path for path in expected_shared_rule_paths if path in existing_shared_rule_paths
        )
        missing_shared_rule_paths = tuple(
            path for path in expected_shared_rule_paths if path not in existing_shared_rule_paths
        )
        return WorkspaceContractSummary(
            project_root=self.project_root,
            target_dir=self.layout.target_dir(self.project_root),
            config_path=self.layout.config_path(self.project_root),
            agentic_dir_exists=self.agentic_dir_exists,
            config_exists=self.config_exists,
            shared_rule_paths=present_shared_rule_paths,
            missing_shared_rule_paths=missing_shared_rule_paths,
            local_paths=self.local_paths,
        )

    def _build_write_plan(
        self,
        *,
        overwrite_shared_rule_documents: bool,
        overwrite_bootstrap_instruction: bool,
    ) -> WorkspaceWritePlan:
        changes: list[SyncChange] = []
        preserved_paths: list[Path] = []

        config_path = self.layout.config_path(self.project_root)
        if self.config_exists:
            preserved_paths.append(config_path)
        else:
            changes.append(
                SyncChange(
                    target_path=config_path,
                    action=SyncAction.CREATE,
                    content=self.config_content,
                )
            )

        bootstrap_instruction_path = self.layout.bootstrap_instruction_path(
            self.project_root)
        if self.bootstrap_instruction_exists:
            if overwrite_bootstrap_instruction:
                changes.append(
                    SyncChange(
                        target_path=bootstrap_instruction_path,
                        action=SyncAction.UPDATE,
                        content=self.bootstrap_instruction_content,
                    )
                )
            else:
                preserved_paths.append(bootstrap_instruction_path)
        else:
            changes.append(
                SyncChange(
                    target_path=bootstrap_instruction_path,
                    action=SyncAction.CREATE,
                    content=self.bootstrap_instruction_content,
                )
            )

        existing_shared_rule_paths = set(self.existing_shared_rule_paths)
        for document in self.shared_rule_documents:
            target_path = self.layout.shared_rule_destination(
                self.project_root,
                document.shared_rule_path,
            )
            if target_path in existing_shared_rule_paths:
                if overwrite_shared_rule_documents:
                    changes.append(
                        SyncChange(
                            target_path=target_path,
                            action=SyncAction.UPDATE,
                            content=document.content,
                            shared_rule_path=document.shared_rule_path,
                        )
                    )
                else:
                    preserved_paths.append(target_path)
                continue

            changes.append(
                SyncChange(
                    target_path=target_path,
                    action=SyncAction.CREATE,
                    content=document.content,
                    shared_rule_path=document.shared_rule_path,
                )
            )

        return WorkspaceWritePlan(
            target_dir=self.layout.target_dir(self.project_root),
            required_dirs=_sort_paths(
                (self.layout.local_dir(self.project_root),)),
            changes=tuple(changes),
            preserved_paths=_sort_paths(tuple(preserved_paths)),
        )


__all__ = ["Workspace"]


def _sort_paths(paths: tuple[Path, ...]) -> tuple[Path, ...]:
    return tuple(sorted(paths, key=lambda path: path.as_posix()))


def _sort_shared_rule_documents(
    documents: tuple[SharedRuleDocument, ...],
) -> tuple[SharedRuleDocument, ...]:
    return tuple(
        sorted(
            documents,
            key=lambda document: document.shared_rule_path.as_posix(),
        )
    )


def _unique_paths(paths: tuple[Path, ...]) -> tuple[Path, ...]:
    return tuple(dict.fromkeys(_sort_paths(paths)))
