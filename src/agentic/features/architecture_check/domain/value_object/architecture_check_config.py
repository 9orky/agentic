from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field, ValidationError, field_validator

from .architecture_check_config_error import ArchitectureCheckConfigError
from .rule_set import RuleSet


class ArchitectureCheckConfig(BaseModel):
    language: Literal["python", "typescript", "php"] = "python"
    exclusions: list[str] = Field(default_factory=list)
    rules: RuleSet = Field(default_factory=RuleSet)

    @field_validator("exclusions")
    @classmethod
    def validate_exclusions(cls, values: list[str]) -> list[str]:
        return [value.strip().replace("\\", "/") for value in values if value.strip()]

    @classmethod
    def validate_mapping(cls, raw_data: object, config_path: Path) -> "ArchitectureCheckConfig":
        try:
            return cls.model_validate(raw_data)
        except ValidationError as exc:
            raise ArchitectureCheckConfigError(
                f"Invalid config values in {config_path}: {exc}") from exc
