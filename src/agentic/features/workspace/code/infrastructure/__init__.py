from pathlib import Path

from .recipe_repository import FileRecipeRepository

recipe_repository = FileRecipeRepository(Path("agentic") / "code")

__all__ = ["FileRecipeRepository", "recipe_repository"]
