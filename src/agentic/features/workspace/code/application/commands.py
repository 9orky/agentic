from __future__ import annotations

from pathlib import Path
from ..domain import RecipeRepository
from .service.recipe_generation import GenerateRecipeResult, build_recipe_generation_service


def generate_recipe(
    recipe_name: str,
    cwd: Path,
    path: Path | str = ".",
    *,
    recipe_root: Path | None = None,
    repository: RecipeRepository | None = None,
) -> GenerateRecipeResult:
    target_root = cwd / path
    target_root.mkdir(parents=True, exist_ok=True)
    return build_recipe_generation_service(recipe_root=recipe_root, repository=repository).generate(recipe_name, target_root)


__all__ = ["GenerateRecipeResult", "generate_recipe"]
