from __future__ import annotations

from pathlib import Path

from ..domain import Recipe, RecipeRepository, RelativePath


class FileRecipeRepository(RecipeRepository):
    def find_all(self) -> tuple[Recipe, ...]:
        if not self.root_path.is_dir():
            return ()

        return tuple(
            self._load_recipe(recipe_root)
            for recipe_root in sorted(self._iter_recipe_roots(), key=lambda path: path.name)
        )

    def get_by_name(self, name: str) -> Recipe:
        recipe_root = self.root_path / name
        if not recipe_root.is_dir():
            raise LookupError(name)

        return self._load_recipe(recipe_root)

    def _iter_recipe_roots(self):
        for child in self.root_path.iterdir():
            if child.name.startswith("."):
                continue
            if child.is_dir():
                yield child

    def _load_recipe(self, recipe_root: Path) -> Recipe:
        return Recipe(
            name=recipe_root.name,
            root_path=recipe_root,
            relative_paths=tuple(self._relative_paths_from(recipe_root)),
        )

    def _relative_paths_from(self, recipe_root: Path) -> tuple[RelativePath, ...]:
        return tuple(
            RelativePath(path.relative_to(recipe_root))
            for path in sorted(recipe_root.rglob("*"), key=lambda path: path.relative_to(recipe_root).as_posix())
        )


__all__ = ["FileRecipeRepository"]
