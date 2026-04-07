from __future__ import annotations

from pathlib import Path
from shutil import copy2
from typing import TypedDict

from agentic.project_layout import AgenticProjectLayout

from ...domain import Recipe, RecipeRepository
from ...infrastructure import FileRecipeRepository


class RecipeGenerationReport(TypedDict):
    recipe_name: str
    cwd: Path
    recipe_found: bool
    recipe_empty: bool
    create_paths: tuple[Path, ...]
    skipped_paths: tuple[Path, ...]


class GenerateRecipeResult(TypedDict):
    recipe_name: str
    cwd: Path
    recipe_found: bool
    recipe_empty: bool
    created_paths: tuple[Path, ...]
    skipped_paths: tuple[Path, ...]


class RecipeGenerationService:
    def __init__(self, *, repository: RecipeRepository) -> None:
        self._repository = repository

    def describe(self, recipe_name: str, cwd: Path) -> RecipeGenerationReport:
        target_root = Path(cwd).resolve()
        recipe = self._load_recipe(recipe_name)
        if recipe is None:
            return {
                "recipe_name": recipe_name,
                "cwd": target_root,
                "recipe_found": False,
                "recipe_empty": False,
                "create_paths": (),
                "skipped_paths": (),
            }

        create_paths, skipped_paths = self._plan_paths(recipe, target_root)
        return {
            "recipe_name": recipe.name,
            "cwd": target_root,
            "recipe_found": True,
            "recipe_empty": recipe.is_empty(),
            "create_paths": create_paths,
            "skipped_paths": skipped_paths,
        }

    def generate(self, recipe_name: str, cwd: Path) -> GenerateRecipeResult:
        report = self.describe(recipe_name, cwd)
        if not report["recipe_found"]:
            return {
                "recipe_name": report["recipe_name"],
                "cwd": report["cwd"],
                "recipe_found": False,
                "recipe_empty": False,
                "created_paths": (),
                "skipped_paths": report["skipped_paths"],
            }

        recipe = self._load_recipe(report["recipe_name"])
        assert recipe is not None
        self._create_missing_paths(
            recipe_root=recipe.root_path,
            target_paths=report["create_paths"],
            cwd=report["cwd"],
        )

        return {
            "recipe_name": report["recipe_name"],
            "cwd": report["cwd"],
            "recipe_found": True,
            "recipe_empty": report["recipe_empty"],
            "created_paths": report["create_paths"],
            "skipped_paths": report["skipped_paths"],
        }

    def _load_recipe(self, recipe_name: str) -> Recipe | None:
        try:
            return self._repository.get_by_name(recipe_name)
        except LookupError:
            return None

    @staticmethod
    def _plan_paths(recipe: Recipe, target_root: Path) -> tuple[tuple[Path, ...], tuple[Path, ...]]:
        create_paths: list[Path] = []
        skipped_paths: list[Path] = []

        for relative_path in recipe.relative_paths:
            target_path = relative_path.resolve_from(target_root)
            if target_path.exists():
                skipped_paths.append(target_path)
                continue

            create_paths.append(target_path)

        return tuple(create_paths), tuple(skipped_paths)

    @staticmethod
    def _create_missing_paths(*, recipe_root: Path, target_paths: tuple[Path, ...], cwd: Path) -> None:
        for target_path in target_paths:
            relative_path = target_path.relative_to(cwd)
            source_path = recipe_root / relative_path
            if source_path.is_dir():
                target_path.mkdir(parents=True, exist_ok=True)
                continue

            target_path.parent.mkdir(parents=True, exist_ok=True)
            copy2(source_path, target_path)


def build_recipe_generation_service(
    *,
    cwd: Path,
    repository: RecipeRepository | None = None,
) -> RecipeGenerationService:
    return RecipeGenerationService(
        repository=repository or FileRecipeRepository(
            _resolve_recipe_root(cwd)),
    )


def _resolve_recipe_root(cwd: Path) -> Path:
    target_root = Path(cwd).resolve()
    layout = AgenticProjectLayout()

    for candidate in (target_root, *target_root.parents):
        code_dir = layout.target_dir(candidate) / "code"
        if code_dir.is_dir():
            return code_dir

        if layout.config_path(candidate).is_file():
            return code_dir

    return layout.target_dir(target_root) / "code"


__all__ = [
    "GenerateRecipeResult",
    "RecipeGenerationReport",
    "RecipeGenerationService",
    "build_recipe_generation_service",
]
