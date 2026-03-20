from __future__ import annotations

from dataclasses import dataclass
from typing import TypeAlias

from pydantic import BaseModel, ValidationError, field_validator


class ExtractorContractError(RuntimeError):
    pass


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


ArchitectureMap: TypeAlias = dict[str, ExtractedFile]


@dataclass(frozen=True)
class ExtractionSummary:
    files_found: int
    files_excluded: int
    files_checked: int


@dataclass(frozen=True)
class ExtractionResult:
    files: ArchitectureMap
    summary: ExtractionSummary


def validate_architecture_map(raw_data: object, source_name: str) -> ExtractionResult:
    if not isinstance(raw_data, dict):
        raise ExtractorContractError(
            f"Extractor output must be a JSON object: {source_name}")

    raw_files = raw_data
    raw_summary: object | None = None
    if set(raw_data.keys()) == {"files", "summary"}:
        raw_files = raw_data["files"]
        raw_summary = raw_data["summary"]

    if not isinstance(raw_files, dict):
        raise ExtractorContractError(
            f"Extractor output 'files' must be a JSON object: {source_name}")

    validated: ArchitectureMap = {}
    for raw_path, raw_entry in raw_files.items():
        if not isinstance(raw_path, str):
            raise ExtractorContractError(
                f"Extractor output paths must be strings: {source_name}")

        normalized_path = raw_path.replace("\\", "/").strip().strip("/")
        if not normalized_path:
            raise ExtractorContractError(
                f"Extractor output paths must not be empty: {source_name}")
        if normalized_path in validated:
            raise ExtractorContractError(
                f"Extractor output contains duplicate normalized paths '{normalized_path}': {source_name}"
            )

        try:
            validated[normalized_path] = ExtractedFile.model_validate(
                raw_entry)
        except ValidationError as exc:
            raise ExtractorContractError(
                f"Invalid extractor output for '{normalized_path}' in {source_name}: {exc}"
            ) from exc

    summary = _validate_summary(raw_summary, source_name, len(validated))
    return ExtractionResult(files=validated, summary=summary)


def _validate_summary(
    raw_summary: object | None,
    source_name: str,
    files_checked: int,
) -> ExtractionSummary:
    if raw_summary is None:
        return ExtractionSummary(
            files_found=files_checked,
            files_excluded=0,
            files_checked=files_checked,
        )

    if not isinstance(raw_summary, dict):
        raise ExtractorContractError(
            f"Extractor output 'summary' must be a JSON object: {source_name}")

    files_found = _validate_summary_count(
        raw_summary, "files_found", source_name)
    files_excluded = _validate_summary_count(
        raw_summary, "files_excluded", source_name)
    reported_checked = _validate_summary_count(
        raw_summary, "files_checked", source_name)

    if reported_checked != files_checked:
        raise ExtractorContractError(
            f"Extractor summary files_checked must match emitted files in {source_name}"
        )

    if files_found < files_excluded + reported_checked:
        raise ExtractorContractError(
            f"Extractor summary counts are inconsistent in {source_name}")

    return ExtractionSummary(
        files_found=files_found,
        files_excluded=files_excluded,
        files_checked=reported_checked,
    )


def _validate_summary_count(raw_summary: dict[object, object], field_name: str, source_name: str) -> int:
    value = raw_summary.get(field_name)
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ExtractorContractError(
            f"Extractor summary field '{field_name}' must be a non-negative integer: {source_name}"
        )
    return value
