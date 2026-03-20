from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field, ValidationError, field_validator

from .domain.normalization import normalize_required_pattern, normalize_pattern_list


class AgenticConfigError(RuntimeError):
    pass


class BoundaryRule(BaseModel):
    source: str
    disallow: list[str] = Field(default_factory=list)
    allow: list[str] = Field(default_factory=list)
    allow_same_match: bool = False

    @field_validator("source")
    @classmethod
    def validate_source(cls, value: str) -> str:
        return normalize_required_pattern(value, field_name="boundary source")

    @field_validator("disallow")
    @classmethod
    def validate_disallow(cls, values: list[str]) -> list[str]:
        return normalize_pattern_list(values)

    @field_validator("allow")
    @classmethod
    def validate_allow(cls, values: list[str]) -> list[str]:
        return normalize_pattern_list(values)


class RuleSet(BaseModel):
    boundaries: list[BoundaryRule] = Field(default_factory=list)


class AgenticConfig(BaseModel):
    language: Literal["python", "typescript", "php"] = "python"
    exclusions: list[str] = Field(default_factory=list)
    rules: RuleSet = Field(default_factory=RuleSet)

    @field_validator("exclusions")
    @classmethod
    def validate_exclusions(cls, values: list[str]) -> list[str]:
        return normalize_pattern_list(values)


@dataclass(frozen=True)
class ConfigLoadResult:
    path: Path
    config: AgenticConfig
    source_format: str


def validate_config_mapping(raw_data: object, config_path: Path) -> AgenticConfig:
    try:
        return AgenticConfig.model_validate(raw_data)
    except ValidationError as exc:
        raise AgenticConfigError(
            f"Invalid config values in {config_path}: {exc}"
        ) from exc
