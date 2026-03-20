from __future__ import annotations

from pathlib import Path

import yaml

from ..contracts import AgenticConfigError


class YamlConfigMappingLoader:
    def load_mapping(self, raw_text: str, config_path: Path) -> tuple[dict[str, object], str]:
        suffix = config_path.suffix.lower()
        if suffix not in {".yaml", ".yml"}:
            raise AgenticConfigError(
                f"Unsupported config format: {config_path.name}")

        try:
            raw_data = yaml.safe_load(raw_text) or {}
        except yaml.YAMLError as exc:
            raise AgenticConfigError(
                f"Invalid config syntax in {config_path}") from exc

        if not isinstance(raw_data, dict):
            raise AgenticConfigError(
                f"Config file must contain a mapping at the top level: {config_path}"
            )

        return raw_data, "yaml"
