from __future__ import annotations

from pathlib import Path

from ..adapters.filesystem import LocalConfigPathResolver, LocalConfigTextReader
from ..adapters.yaml import YamlConfigMappingLoader
from ..contracts import AgenticConfigError, ConfigLoadResult, validate_config_mapping
from ..ports import ConfigMappingLoader, ConfigPathResolver, ConfigTextReader


def load_config(
    project_root: Path,
    explicit_config_path: str | None = None,
    *,
    path_resolver: ConfigPathResolver | None = None,
    text_reader: ConfigTextReader | None = None,
    mapping_loader: ConfigMappingLoader | None = None,
) -> ConfigLoadResult:
    resolver = path_resolver or LocalConfigPathResolver()
    reader = text_reader or LocalConfigTextReader()
    loader = mapping_loader or YamlConfigMappingLoader()

    config_path = resolver.resolve(project_root, explicit_config_path)
    if config_path is None:
        raise AgenticConfigError(
            "Could not find a configuration file. Expected agentic/agentic.yaml or agentic.yml."
        )

    raw_text = reader.read_text(config_path)
    raw_data, source_format = loader.load_mapping(raw_text, config_path)
    config = validate_config_mapping(raw_data, config_path)
    return ConfigLoadResult(path=config_path, config=config, source_format=source_format)
