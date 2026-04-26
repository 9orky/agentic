from __future__ import annotations

from dataclasses import dataclass
from math import sqrt

from ..domain import ExtractionResult
from .queries import BuildDependencyMapResult


@dataclass(frozen=True)
class ArchitectureRiskSignal:
    name: str
    raw_value: float
    score: float


@dataclass(frozen=True)
class FileArchitectureMetrics:
    path: str
    imports_count: int
    imported_by_count: int
    class_count: int
    function_count: int
    method_count: int
    symbol_count: int
    line_count: int
    code_line_count: int
    public_symbol_count: int
    max_method_count_per_class: int
    risk_score: float
    dominant_signals: tuple[str, ...]
    risk_signals: tuple[ArchitectureRiskSignal, ...]


def derive_file_architecture_metrics(
    result: BuildDependencyMapResult,
) -> tuple[FileArchitectureMetrics, ...]:
    tracked_files = tuple(result.extraction_result.files.keys())
    imports_by_file = {file_path: set() for file_path in tracked_files}
    imported_by_file = {file_path: set() for file_path in tracked_files}

    for edge in result.graph.edges:
        if edge.from_id not in imports_by_file or edge.to_id not in imported_by_file:
            continue
        imports_by_file[edge.from_id].add(edge.to_id)
        imported_by_file[edge.to_id].add(edge.from_id)

    return tuple(
        _build_file_metrics(
            file_path,
            result.extraction_result,
            imports_count=len(imports_by_file[file_path]),
            imported_by_count=len(imported_by_file[file_path]),
        )
        for file_path in tracked_files
    )


def _build_file_metrics(
    file_path: str,
    extraction_result: ExtractionResult,
    *,
    imports_count: int,
    imported_by_count: int,
) -> FileArchitectureMetrics:
    extracted_file = extraction_result.files[file_path]
    class_count = len(extracted_file.class_details) or len(extracted_file.classes)
    function_count = len(extracted_file.function_details) or len(extracted_file.functions)
    method_count = sum(len(class_detail.methods) for class_detail in extracted_file.class_details)
    symbol_count = class_count + function_count + method_count
    metrics = extracted_file.metrics
    line_count = metrics.line_count if metrics and metrics.line_count is not None else 0
    code_line_count = (
        metrics.code_line_count if metrics and metrics.code_line_count is not None else 0
    )
    public_symbol_count = (
        metrics.public_symbol_count
        if metrics and metrics.public_symbol_count is not None
        else class_count + function_count
    )
    max_method_count_per_class = (
        metrics.max_method_count_per_class
        if metrics and metrics.max_method_count_per_class is not None
        else max((len(class_detail.methods) for class_detail in extracted_file.class_details), default=0)
    )
    risk_signals = (
        ArchitectureRiskSignal(
            name="incoming imports",
            raw_value=float(imported_by_count),
            score=round(4.2 * sqrt(imported_by_count), 2),
        ),
        ArchitectureRiskSignal(
            name="outgoing imports",
            raw_value=float(imports_count),
            score=round(2.4 * sqrt(imports_count), 2),
        ),
        ArchitectureRiskSignal(
            name="symbol surface",
            raw_value=float(symbol_count),
            score=round(2.0 * sqrt(symbol_count), 2),
        ),
        ArchitectureRiskSignal(
            name="public API surface",
            raw_value=float(public_symbol_count),
            score=round(2.8 * sqrt(public_symbol_count), 2),
        ),
        ArchitectureRiskSignal(
            name="implementation size",
            raw_value=float(code_line_count),
            score=round(2.1 * sqrt(code_line_count / 20.0), 2) if code_line_count else 0.0,
        ),
        ArchitectureRiskSignal(
            name="class density",
            raw_value=float(max_method_count_per_class),
            score=round(1.9 * sqrt(max_method_count_per_class), 2),
        ),
        ArchitectureRiskSignal(
            name="dependency skew",
            raw_value=float(abs(imported_by_count - imports_count)),
            score=round(1.6 * sqrt(abs(imported_by_count - imports_count)), 2),
        ),
    )
    dominant_signals = tuple(
        signal.name
        for signal in sorted(
            risk_signals,
            key=lambda item: (-item.score, item.name),
        )
        if signal.score > 0
    )[:3]
    risk_score = round(sum(signal.score for signal in risk_signals), 2)

    return FileArchitectureMetrics(
        path=file_path,
        imports_count=imports_count,
        imported_by_count=imported_by_count,
        class_count=class_count,
        function_count=function_count,
        method_count=method_count,
        symbol_count=symbol_count,
        line_count=line_count,
        code_line_count=code_line_count,
        public_symbol_count=public_symbol_count,
        max_method_count_per_class=max_method_count_per_class,
        risk_score=risk_score,
        dominant_signals=dominant_signals,
        risk_signals=risk_signals,
    )


__all__ = [
    "ArchitectureRiskSignal",
    "FileArchitectureMetrics",
    "derive_file_architecture_metrics",
]
