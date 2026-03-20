from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import sys

from ...configuration import load_config
from ..contracts import ArchitectureSummary, CheckResult, CheckerError
from ..domain.evaluation import evaluate_boundary_violations
from ..ports import ExtractorRuntime, ExtractorSpec


@dataclass(frozen=True)
class _LanguageRuntime:
    command: str
    resource_name: str


_EXTRACTOR_SPECS: dict[str, _LanguageRuntime] = {
    "python": _LanguageRuntime(command=sys.executable, resource_name="python_extractor.py"),
    "typescript": _LanguageRuntime(command="node", resource_name="typescript_extractor.js"),
    "php": _LanguageRuntime(command="php", resource_name="php_extractor.php"),
}


def run_architecture_check(
    project_root: Path,
    explicit_config_path: str | None,
    *,
    extractor_runtime: ExtractorRuntime,
) -> CheckResult:
    summary = describe_architecture(
        project_root,
        explicit_config_path,
        extractor_runtime=extractor_runtime,
    )
    if summary.check_error is not None:
        raise CheckerError(summary.check_error)

    return CheckResult(
        project_root=summary.project_root,
        config_path=summary.config_path,
        config_format=summary.config_format,
        files_found=summary.files_found,
        files_excluded=summary.files_excluded,
        files_checked=summary.files_checked,
        violations=list(summary.violations),
    )


def describe_architecture(
    project_root: Path,
    explicit_config_path: str | None,
    *,
    extractor_runtime: ExtractorRuntime,
) -> ArchitectureSummary:
    try:
        load_result = load_config(project_root, explicit_config_path)
    except RuntimeError as exc:
        raise CheckerError(str(exc)) from exc

    runtime = _EXTRACTOR_SPECS.get(load_result.config.language)
    if runtime is None:
        raise CheckerError(
            f"Unsupported language '{load_result.config.language}'")

    try:
        extraction_result = extractor_runtime.run(
            ExtractorSpec(command=runtime.command,
                          resource_name=runtime.resource_name),
            project_root,
            load_result.config.exclusions,
        )
    except CheckerError as exc:
        return ArchitectureSummary(
            project_root=project_root,
            config_path=load_result.path,
            config_format=load_result.source_format,
            language=load_result.config.language,
            runtime_command=runtime.command,
            check_error=str(exc),
        )

    violations = evaluate_boundary_violations(
        extraction_result.files, load_result.config)
    return ArchitectureSummary(
        project_root=project_root,
        config_path=load_result.path,
        config_format=load_result.source_format,
        language=load_result.config.language,
        runtime_command=runtime.command,
        files_found=extraction_result.summary.files_found,
        files_excluded=extraction_result.summary.files_excluded,
        files_checked=extraction_result.summary.files_checked,
        violations=tuple(violations),
    )
