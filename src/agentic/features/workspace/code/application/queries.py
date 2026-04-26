from __future__ import annotations

from collections.abc import Callable
from pathlib import Path

from ..domain import CodeGenerationConfig, RecipeRepository
from .service.recipe_generation import RecipeGenerationReport, build_recipe_generation_service, load_code_generation_config


def describe_recipe_generation(
    recipe_name: str,
    cwd: Path,
    path: Path | str = ".",
    *,
    recipe_root: Path | None = None,
    repository: RecipeRepository | None = None,
    config: CodeGenerationConfig | None = None,
) -> RecipeGenerationReport:
    return build_recipe_generation_service(
        recipe_root=recipe_root,
        repository=repository,
        config=config,
    ).describe(recipe_name, cwd / path)


def load_code_generation_settings(
    *,
    project_root: Path,
    config_candidate_paths: Callable[[Path], tuple[Path, ...]],
) -> CodeGenerationConfig:
    return load_code_generation_config(
        project_root=project_root,
        config_candidate_paths=config_candidate_paths,
    )


__all__ = ["RecipeGenerationReport",
           "describe_recipe_generation", "load_code_generation_settings"]
