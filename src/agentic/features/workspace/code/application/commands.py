from __future__ import annotations

from pathlib import Path
from ..domain import RecipeRepository
from .service.recipe_generation import GenerateRecipeResult, build_recipe_generation_service


def generate_recipe(
    recipe_name: str,
    cwd: Path,
    *,
    repository: RecipeRepository | None = None,
) -> GenerateRecipeResult:
    return build_recipe_generation_service(cwd=cwd, repository=repository).generate(recipe_name, cwd)


__all__ = ["GenerateRecipeResult", "generate_recipe"]
