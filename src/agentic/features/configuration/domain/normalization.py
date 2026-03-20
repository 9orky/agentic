from __future__ import annotations


def normalize_required_pattern(value: str, *, field_name: str) -> str:
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must not be empty")
    return normalized.replace("\\", "/")


def normalize_pattern_list(values: list[str]) -> list[str]:
    return [value.strip().replace("\\", "/") for value in values if value.strip()]
