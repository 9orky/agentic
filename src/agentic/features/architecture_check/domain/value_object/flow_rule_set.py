from typing import Literal

from pydantic import BaseModel, Field, field_validator


class FlowRuleSet(BaseModel):
    layers: list[str] = Field(default_factory=list)
    module_tag: str = "module"
    analyzers: list[Literal["backward-flow", "no-reentry",
                            "no-cycles"]] = Field(default_factory=list)

    @field_validator("layers")
    @classmethod
    def validate_layers(cls, values: list[str]) -> list[str]:
        normalized: list[str] = []
        for value in values:
            stripped = value.strip()
            if not stripped:
                raise ValueError("flow layers must not contain empty values")
            normalized.append(stripped)
        return normalized

    @field_validator("module_tag")
    @classmethod
    def validate_module_tag(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("flow module_tag must not be empty")
        return normalized
