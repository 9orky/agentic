from __future__ import annotations

from pathlib import Path

from ...domain import ConfigLoadResult
from ..services.config_load_service import ConfigLoadService, build_default_config_load_service


class LoadConfigQuery:
    def __init__(self, *, config_load_service: ConfigLoadService) -> None:
        self._config_load_service = config_load_service

    def load(
        self,
        project_root: Path,
        explicit_config_path: str | None = None,
    ) -> ConfigLoadResult:
        return self._config_load_service.load(project_root, explicit_config_path)


def build_default_load_config_query() -> LoadConfigQuery:
    return LoadConfigQuery(
        config_load_service=build_default_config_load_service(),
    )


load_config = build_default_load_config_query().load

__all__ = ["LoadConfigQuery", "load_config"]
