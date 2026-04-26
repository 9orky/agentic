from __future__ import annotations

from pathlib import Path
from ..domain import RecipeRepository
from .service.recipe_generation import RecipeGenerationReport, build_recipe_generation_service


def describe_recipe_generation(
    recipe_name: str,
    cwd: Path,
    path: Path | str = ".",
    *,
    recipe_root: Path | None = None,
    repository: RecipeRepository | None = None,
) -> RecipeGenerationReport:
    return build_recipe_generation_service(recipe_root=recipe_root, repository=repository).describe(recipe_name, cwd / path)


__all__ = ["RecipeGenerationReport", "describe_recipe_generation"]
