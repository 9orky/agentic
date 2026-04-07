from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path
from typing import Any


class CodeGenerationView:
    def render_generate_result(self, result: Mapping[str, Any], *, project_root: Path) -> tuple[str, ...]:
        if not result["recipe_found"]:
            return (f"Recipe not found: agentic/code/{result['recipe_name']}/.",)

        lines = [f"Generated recipe '{result['recipe_name']}'."]
        lines.extend(
            self._render_path_details(
                created_label="Created",
                created_paths=result["created_paths"],
                skipped_paths=result["skipped_paths"],
                project_root=project_root,
            )
        )
        if result["recipe_empty"]:
            lines.append(
                f"Warning: recipe '{result['recipe_name']}' is empty.")
        return tuple(lines)

    def render_dry_run_result(self, result: Mapping[str, Any], *, project_root: Path) -> tuple[str, ...]:
        if not result["recipe_found"]:
            return (f"Recipe not found: agentic/code/{result['recipe_name']}/.",)

        lines = [f"Dry run for recipe '{result['recipe_name']}'."]
        lines.extend(
            self._render_path_details(
                created_label="Would create",
                created_paths=result["create_paths"],
                skipped_paths=result["skipped_paths"],
                project_root=project_root,
            )
        )
        if result["recipe_empty"]:
            lines.append(
                f"Warning: recipe '{result['recipe_name']}' is empty.")
        return tuple(lines)

    def _render_path_details(
        self,
        *,
        created_label: str,
        created_paths: tuple[Path, ...],
        skipped_paths: tuple[Path, ...],
        project_root: Path,
    ) -> tuple[str, ...]:
        lines: list[str] = []
        if created_paths:
            lines.append(f"{created_label} {len(created_paths)} path(s).")
            lines.extend(self._render_path_list(
                created_paths, project_root=project_root))
        if skipped_paths:
            lines.append(f"Skipped {len(skipped_paths)} existing path(s).")
            lines.extend(self._render_path_list(
                skipped_paths, project_root=project_root))
        if not created_paths and not skipped_paths:
            lines.append("No changes.")
        return tuple(lines)

    def _render_path_list(self, paths: tuple[Path, ...], *, project_root: Path) -> tuple[str, ...]:
        return tuple(f"- {_present_path(path, project_root=project_root)}" for path in paths)


def build_default_code_generation_view() -> CodeGenerationView:
    return CodeGenerationView()


def _present_path(path: Path, *, project_root: Path) -> str:
    try:
        return path.relative_to(project_root).as_posix()
    except ValueError:
        return str(path)


__all__ = ["CodeGenerationView", "build_default_code_generation_view"]
