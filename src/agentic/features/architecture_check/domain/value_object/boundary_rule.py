from pydantic import BaseModel, Field, field_validator


class BoundaryRule(BaseModel):
    source: str
    disallow: list[str] = Field(default_factory=list)
    allow: list[str] = Field(default_factory=list)
    allow_same_match: bool = False

    @field_validator("source")
    @classmethod
    def validate_source(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("boundary source must not be empty")
        return normalized.replace("\\", "/")

    @field_validator("disallow")
    @classmethod
    def validate_disallow(cls, values: list[str]) -> list[str]:
        return [value.strip().replace("\\", "/") for value in values if value.strip()]

    @field_validator("allow")
    @classmethod
    def validate_allow(cls, values: list[str]) -> list[str]:
        return [value.strip().replace("\\", "/") for value in values if value.strip()]
