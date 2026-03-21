from dataclasses import dataclass


@dataclass(frozen=True)
class ExtractionSummary:
    files_found: int
    files_excluded: int
    files_checked: int
