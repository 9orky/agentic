from pydantic import BaseModel, field_validator


class ConfigTagRule(BaseModel):
    name: str
    match: str

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("tag name must not be empty")
        return normalized

    @field_validator("match")
    @classmethod
    def validate_match(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("tag match must not be empty")
        return normalized.replace("\\", "/")
