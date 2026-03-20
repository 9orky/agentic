from __future__ import annotations

from ...configuration import AgenticConfig
from .extractor_contract import ArchitectureMap
from .patterns import match_exact_pattern, match_scope_pattern, normalize_import_reference


def evaluate_boundary_violations(architecture_map: ArchitectureMap, config: AgenticConfig) -> list[str]:
    violations: list[str] = []
    for file_path, data in architecture_map.items():
        normalized_path = file_path.replace("\\", "/")
        for boundary in config.rules.boundaries:
            source_match = match_scope_pattern(
                normalized_path, boundary.source)
            if source_match is None:
                continue
            for imported in data.imports:
                imported_reference = normalize_import_reference(imported)
                if any(match_exact_pattern(imported_reference, allowed) is not None for allowed in boundary.allow):
                    continue
                for disallowed in boundary.disallow:
                    disallowed_match = match_scope_pattern(
                        imported_reference, disallowed)
                    if disallowed_match is None:
                        continue
                    if (
                        boundary.allow_same_match
                        and source_match.captures
                        and source_match.captures == disallowed_match.captures
                    ):
                        continue
                    violations.append(
                        f"[VIOLATION] {file_path}\n"
                        f"  -> Layer '{boundary.source}' cannot depend on '{disallowed}'\n"
                        f"  -> Offending import: '{imported_reference}'"
                    )
                    break
    return violations
