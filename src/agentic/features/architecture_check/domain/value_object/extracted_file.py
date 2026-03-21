from pydantic import BaseModel, field_validator


class ExtractedFile(BaseModel):
    imports: list[str]
    classes: list[str]
    functions: list[str]

    @field_validator("imports", "classes", "functions")
    @classmethod
    def validate_string_list(cls, values: list[str]) -> list[str]:
        normalized: list[str] = []
        for value in values:
            if not isinstance(value, str):
                raise ValueError("extractor fields must contain only strings")
            stripped = value.strip()
            if stripped:
                normalized.append(stripped)
        return normalized
