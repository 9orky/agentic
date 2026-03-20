from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
import re


@dataclass(frozen=True)
class PatternMatch:
    captures: tuple[str, ...]


def normalize_path_pattern(value: str) -> str:
    return value.replace("\\", "/").strip().strip("/")


def normalize_import_reference(value: str) -> str:
    normalized = value.replace("\\", "/").strip()
    if "/" not in normalized and not normalized.startswith("."):
        normalized = normalized.replace(".", "/")
    return normalized.strip("/")


def match_scope_pattern(value: str, pattern: str) -> PatternMatch | None:
    return _match_pattern(value, pattern, scope=True)


def match_exact_pattern(value: str, pattern: str) -> PatternMatch | None:
    return _match_pattern(value, pattern, scope=False)


def _match_pattern(value: str, pattern: str, scope: bool) -> PatternMatch | None:
    normalized_value = normalize_path_pattern(value)
    normalized_pattern = normalize_path_pattern(pattern)
    if not normalized_pattern:
        return None

    match = _compile_pattern(normalized_pattern, scope).match(normalized_value)
    if match is None:
        return None
    return PatternMatch(captures=match.groups())


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