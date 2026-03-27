from __future__ import annotations

from pathlib import Path

from ...domain.value_object import ArchitectureCheckConfig, ArchitectureCheckConfigError, ConfigLoadResult
from ...infrastructure import ConfigLoader


class LoadConfigQuery:
    def __init__(self, *, config_loader: ConfigLoader) -> None:
        self._config_loader = config_loader

    def load(
        self,
        project_root: Path,
        explicit_config_path: str | None = None,
    ) -> ConfigLoadResult:
        config_path = self._config_loader.resolve_path(
            project_root, explicit_config_path)
        if config_path is None:
            raise ArchitectureCheckConfigError(
                "Could not find a configuration file. "
                f"Looked for an explicit path, {self._config_loader.config_search_description()}."
            )

        raw_text = self._config_loader.read_text(config_path)
        raw_data, source_format = self._config_loader.load_mapping(
            raw_text, config_path)
        config = ArchitectureCheckConfig.validate_mapping(
            raw_data, config_path)
        return ConfigLoadResult(path=config_path, config=config, source_format=source_format)


def build_default_load_config_query() -> LoadConfigQuery:
    return LoadConfigQuery(config_loader=ConfigLoader())


load_config = build_default_load_config_query().load

__all__ = ["LoadConfigQuery", "load_config"]
