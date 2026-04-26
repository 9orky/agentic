from __future__ import annotations

from collections.abc import Callable
from pathlib import Path

import yaml

from ..domain import CodeGenerationConfig


class FileCodeGenerationConfigLoader:
    def __init__(
        self,
        *,
        config_candidate_paths: Callable[[Path], tuple[Path, ...]],
    ) -> None:
        self._config_candidate_paths = config_candidate_paths

    def load(self, project_root: Path) -> CodeGenerationConfig:
        config_path = self._resolve_path(project_root)
        if config_path is None:
            return CodeGenerationConfig()

        try:
            raw_text = config_path.read_text(encoding="utf-8")
        except OSError as exc:
            raise ValueError(
                f"Could not read config file: {config_path}") from exc

        try:
            raw_data = yaml.safe_load(raw_text) or {}
        except yaml.YAMLError as exc:
            raise ValueError(
                f"Invalid config syntax in {config_path}") from exc

        if not isinstance(raw_data, dict):
            raise ValueError(
                f"Config file must contain a mapping at the top level: {config_path}"
            )

        code_section = raw_data.get("code", {})
        if code_section is None:
            return CodeGenerationConfig()
        if not isinstance(code_section, dict):
            raise ValueError(
                f"Invalid config values in {config_path}: code must be a mapping"
            )

        skip_section = code_section.get("skip", [])
        if skip_section is None:
            return CodeGenerationConfig()
        if not isinstance(skip_section, list) or any(not isinstance(item, str) for item in skip_section):
            raise ValueError(
                f"Invalid config values in {config_path}: code.skip must be a list of strings"
            )

        return CodeGenerationConfig(skip_globs=tuple(skip_section))

    def _resolve_path(self, project_root: Path) -> Path | None:
        seen: set[Path] = set()
        for candidate_root in (project_root.resolve(), *project_root.resolve().parents):
            for candidate in self._config_candidate_paths(candidate_root):
                normalized_candidate = candidate.resolve(strict=False)
                if normalized_candidate in seen:
                    continue
                seen.add(normalized_candidate)
                if normalized_candidate.exists():
                    return normalized_candidate
        return None


__all__ = ["FileCodeGenerationConfigLoader"]
