from __future__ import annotations

from pathlib import Path

import yaml
from agentic.project_layout import AgenticProjectLayout

from ..domain import ArchitectureCheckConfigError


class ConfigLoader:
    def __init__(self, layout: AgenticProjectLayout | None = None) -> None:
        self._layout = layout or AgenticProjectLayout()

    def resolve_path(self, project_root: Path, explicit_config_path: str | None = None) -> Path | None:
        candidates: list[Path] = []
        if explicit_config_path:
            candidates.append(
                Path(explicit_config_path).expanduser().resolve())

        candidates.extend(self._layout.config_candidate_paths(project_root))

        seen: set[Path] = set()
        for candidate in candidates:
            normalized = candidate.resolve(strict=False)
            if normalized in seen:
                continue
            seen.add(normalized)
            if normalized.exists():
                return normalized
        return None

    def config_search_description(self) -> str:
        return ", ".join(self._layout.config_candidate_labels())

    def read_text(self, path: Path) -> str:
        try:
            return path.read_text(encoding="utf-8")
        except OSError as exc:
            raise ArchitectureCheckConfigError(
                f"Could not read config file: {path}") from exc

    def load_mapping(self, raw_text: str, config_path: Path) -> tuple[dict[str, object], str]:
        suffix = config_path.suffix.lower()
        if suffix not in {".yaml", ".yml"}:
            raise ArchitectureCheckConfigError(
                f"Unsupported config format: {config_path.name}")

        try:
            raw_data = yaml.safe_load(raw_text) or {}
        except yaml.YAMLError as exc:
            raise ArchitectureCheckConfigError(
                f"Invalid config syntax in {config_path}") from exc

        if not isinstance(raw_data, dict):
            raise ArchitectureCheckConfigError(
                f"Config file must contain a mapping at the top level: {config_path}"
            )

        return raw_data, "yaml"
