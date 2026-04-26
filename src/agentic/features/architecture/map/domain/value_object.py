from __future__ import annotations

import re
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Literal, Mapping

from pydantic import BaseModel, Field, ValidationError, field_validator


class ArchitectureConfigError(RuntimeError):
    pass


class CheckerError(RuntimeError):
    pass


class ExtractorContractError(RuntimeError):
    pass


@dataclass(frozen=True)
class PatternMatch:
    captures: tuple[str, ...]


class NodeSelector:
    def __init__(
        self,
        path_pattern: str | None = None,
        path_mode: str = "scope",
        tag: str | None = None,
    ) -> None:
        self.path_pattern = path_pattern
        self.path_mode = path_mode
        self.tag = tag

    def matches(
        self,
        node_id: str,
        tags: Mapping[str, set[str]] | None = None,
    ) -> PatternMatch | None:
        if self.tag is not None:
            node_tags = tags.get(node_id, set()) if tags is not None else set()
            if self.tag not in node_tags:
                return None

        if self.path_pattern is None:
            return PatternMatch(())

        return self._match_pattern(node_id, self.path_pattern, scope=self.path_mode != "exact")

    @classmethod
    def normalize_import_reference(cls, value: str) -> str:
        normalized = value.replace("\\", "/").strip()
        if "/" not in normalized and not normalized.startswith("."):
            normalized = normalized.replace(".", "/")
        return normalized.strip("/")

    @classmethod
    def _normalize_path_pattern(cls, value: str) -> str:
        return value.replace("\\", "/").strip().strip("/")

    @classmethod
    def _match_pattern(cls, value: str, pattern: str, *, scope: bool) -> PatternMatch | None:
        normalized_value = cls._normalize_path_pattern(value)
        normalized_pattern = cls._normalize_path_pattern(pattern)
        if not normalized_pattern:
            return None

        match = cls._compile_pattern(normalized_pattern, scope).match(normalized_value)
        if match is None:
            return None
        return PatternMatch(captures=match.groups())

    @staticmethod
    @lru_cache(maxsize=None)
    def _compile_pattern(pattern: str, scope: bool) -> re.Pattern[str]:
        regex_parts = ["^"]
        index = 0

        while index < len(pattern):
            current = pattern[index]
            if current == "*":
                if index + 1 < len(pattern) and pattern[index + 1] == "*":
                    regex_parts.append("(.*)")
                    index += 2
                    continue
                regex_parts.append("([^/]*)")
                index += 1
                continue
            if current == "?":
                regex_parts.append("([^/])")
                index += 1
                continue

            regex_parts.append(re.escape(current))
            index += 1

        if scope:
            regex_parts.append("(?:/.*)?")
        regex_parts.append("$")
        return re.compile("".join(regex_parts))


@dataclass(frozen=True)
class DependencyRule:
    name: str
    source: NodeSelector
    target: NodeSelector
    decision: str
    allow_same_match: bool = False


@dataclass(frozen=True)
class EdgeRuleViolation:
    source_id: str
    target_id: str
    source_pattern: str
    target_pattern: str
    rule_name: str


@dataclass(frozen=True)
class FlowViolation:
    violation_type: str
    path: tuple[str, ...]
    violation_index: int
    rule_name: str
    message: str


@dataclass(frozen=True)
class ExtractionSummary:
    files_found: int
    files_excluded: int
    files_checked: int


@dataclass(frozen=True)
class FlowAnalyzerConfig:
    layers: tuple[str, ...]
    module_tag: str


@dataclass(frozen=True)
class TagRule:
    name: str
    match: str


@dataclass(frozen=True)
class ExtractedMethod:
    name: str
    line_count: int | None = None


@dataclass(frozen=True)
class ExtractedFunction:
    name: str
    line_count: int | None = None
    cyclomatic_complexity: int | None = None


@dataclass(frozen=True)
class ExtractedClass:
    name: str
    methods: tuple[ExtractedMethod, ...] = ()
    line_count: int | None = None


@dataclass(frozen=True)
class FileMetricSet:
    line_count: int | None = None
    code_line_count: int | None = None
    public_symbol_count: int | None = None
    max_method_count_per_class: int | None = None


class ExtractedFile(BaseModel):
    imports: list[str]
    classes: list[str]
    functions: list[str]
    class_details: tuple[ExtractedClass, ...] = ()
    function_details: tuple[ExtractedFunction, ...] = ()
    metrics: FileMetricSet | None = None

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

    @field_validator("class_details")
    @classmethod
    def validate_class_details(
        cls,
        values: tuple[ExtractedClass, ...],
    ) -> tuple[ExtractedClass, ...]:
        seen: set[str] = set()
        normalized: list[ExtractedClass] = []
        for value in values:
            name = value.name.strip()
            if not name or name in seen:
                continue
            cls._validate_optional_count(value.line_count, "class_details.line_count")
            method_names: set[str] = set()
            normalized_methods: list[ExtractedMethod] = []
            for method in value.methods:
                method_name = method.name.strip()
                if not method_name:
                    raise ValueError("class_details.methods.name must not be empty")
                if method_name in method_names:
                    continue
                method_names.add(method_name)
                cls._validate_optional_count(
                    method.line_count,
                    "class_details.methods.line_count",
                )
                normalized_methods.append(method)
            seen.add(name)
            normalized.append(
                ExtractedClass(
                    name=name,
                    methods=tuple(normalized_methods),
                    line_count=value.line_count,
                )
            )
        return tuple(normalized)

    @field_validator("function_details")
    @classmethod
    def validate_function_details(
        cls,
        values: tuple[ExtractedFunction, ...],
    ) -> tuple[ExtractedFunction, ...]:
        seen: set[str] = set()
        normalized: list[ExtractedFunction] = []
        for value in values:
            name = value.name.strip()
            if not name or name in seen:
                continue
            cls._validate_optional_count(
                value.line_count,
                "function_details.line_count",
            )
            cls._validate_optional_count(
                value.cyclomatic_complexity,
                "function_details.cyclomatic_complexity",
            )
            seen.add(name)
            normalized.append(value)
        return tuple(normalized)

    @field_validator("metrics")
    @classmethod
    def validate_metrics(cls, value: FileMetricSet | None) -> FileMetricSet | None:
        if value is None:
            return None
        for field_name in (
            "line_count",
            "code_line_count",
            "public_symbol_count",
            "max_method_count_per_class",
        ):
            cls._validate_optional_count(getattr(value, field_name), f"metrics.{field_name}")
        return value

    def model_post_init(self, __context: object) -> None:
        if not self.classes and self.class_details:
            self.classes.extend(class_detail.name for class_detail in self.class_details)
        if not self.functions and self.function_details:
            self.functions.extend(
                function_detail.name for function_detail in self.function_details
            )

    @staticmethod
    def _validate_optional_count(value: int | None, field_name: str) -> None:
        if value is not None and value < 0:
            raise ValueError(f"{field_name} must be non-negative")


@dataclass(frozen=True)
class ExtractionResult:
    files: dict[str, ExtractedFile]
    summary: ExtractionSummary

    @classmethod
    def validate_output(cls, raw_data: object, source_name: str) -> "ExtractionResult":
        if not isinstance(raw_data, dict):
            raise ExtractorContractError(
                f"Extractor output must be a JSON object: {source_name}"
            )

        raw_files = raw_data
        raw_summary: object | None = None
        if set(raw_data.keys()) == {"files", "summary"}:
            raw_files = raw_data["files"]
            raw_summary = raw_data["summary"]

        if not isinstance(raw_files, dict):
            raise ExtractorContractError(
                f"Extractor output 'files' must be a JSON object: {source_name}"
            )

        validated: dict[str, ExtractedFile] = {}
        for raw_path, raw_entry in raw_files.items():
            if not isinstance(raw_path, str):
                raise ExtractorContractError(
                    f"Extractor output paths must be strings: {source_name}"
                )

            normalized_path = raw_path.replace("\\", "/").strip().strip("/")
            if not normalized_path:
                raise ExtractorContractError(
                    f"Extractor output paths must not be empty: {source_name}"
                )
            if normalized_path in validated:
                raise ExtractorContractError(
                    "Extractor output contains duplicate normalized paths "
                    f"'{normalized_path}': {source_name}"
                )

            try:
                validated[normalized_path] = ExtractedFile.model_validate(raw_entry)
            except ValidationError as exc:
                raise ExtractorContractError(
                    f"Invalid extractor output for '{normalized_path}' in {source_name}: {exc}"
                ) from exc

        return cls(
            files=validated,
            summary=cls._validate_summary(raw_summary, source_name, len(validated)),
        )

    @classmethod
    def _validate_summary(
        cls,
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
                f"Extractor output 'summary' must be a JSON object: {source_name}"
            )

        files_found = cls._validate_summary_count(raw_summary, "files_found", source_name)
        files_excluded = cls._validate_summary_count(raw_summary, "files_excluded", source_name)
        reported_checked = cls._validate_summary_count(raw_summary, "files_checked", source_name)

        if reported_checked != files_checked:
            raise ExtractorContractError(
                f"Extractor summary files_checked must match emitted files in {source_name}"
            )

        if files_found < files_excluded + reported_checked:
            raise ExtractorContractError(
                f"Extractor summary counts are inconsistent in {source_name}"
            )

        return ExtractionSummary(
            files_found=files_found,
            files_excluded=files_excluded,
            files_checked=reported_checked,
        )

    @staticmethod
    def _validate_summary_count(
        raw_summary: dict[object, object],
        field_name: str,
        source_name: str,
    ) -> int:
        value = raw_summary.get(field_name)
        if isinstance(value, bool) or not isinstance(value, int) or value < 0:
            raise ExtractorContractError(
                f"Extractor summary field '{field_name}' must be a non-negative integer: {source_name}"
            )
        return value


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


class FlowRuleSet(BaseModel):
    layers: list[str] = Field(default_factory=list)
    module_tag: str = "module"
    analyzers: list[Literal["backward-flow", "no-reentry", "no-cycles"]] = Field(
        default_factory=list
    )

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


class RuleSet(BaseModel):
    boundaries: list[BoundaryRule] = Field(default_factory=list)
    tags: list[ConfigTagRule] = Field(default_factory=list)
    flow: FlowRuleSet = Field(default_factory=FlowRuleSet)


class ArchitectureConfig(BaseModel):
    language: Literal["python", "typescript", "php"] = "python"
    exclusions: list[str] = Field(default_factory=list)
    rules: RuleSet = Field(default_factory=RuleSet)

    @field_validator("exclusions")
    @classmethod
    def validate_exclusions(cls, values: list[str]) -> list[str]:
        return [value.strip().replace("\\", "/") for value in values if value.strip()]

    @classmethod
    def validate_mapping(cls, raw_data: object, config_path: Path) -> "ArchitectureConfig":
        try:
            return cls.model_validate(raw_data)
        except ValidationError as exc:
            raise ArchitectureConfigError(
                f"Invalid config values in {config_path}: {exc}"
            ) from exc


@dataclass(frozen=True)
class ConfigLoadResult:
    path: Path
    config: ArchitectureConfig
    source_format: str


__all__ = [
    "ArchitectureConfig",
    "ArchitectureConfigError",
    "BoundaryRule",
    "CheckerError",
    "ConfigLoadResult",
    "ConfigTagRule",
    "DependencyRule",
    "EdgeRuleViolation",
    "ExtractedClass",
    "ExtractedFile",
    "ExtractedFunction",
    "ExtractedMethod",
    "ExtractionResult",
    "ExtractionSummary",
    "ExtractorContractError",
    "FileMetricSet",
    "FlowAnalyzerConfig",
    "FlowRuleSet",
    "FlowViolation",
    "NodeSelector",
    "PatternMatch",
    "RuleSet",
    "TagRule",
]
