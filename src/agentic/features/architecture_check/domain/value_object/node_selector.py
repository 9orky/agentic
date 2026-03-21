from __future__ import annotations

from functools import lru_cache
from typing import Mapping, Set
import re

from .pattern_match import PatternMatch


class NodeSelector:
    def __init__(self, path_pattern: str | None = None, path_mode: str = "scope", tag: str | None = None) -> None:
        self.path_pattern = path_pattern
        self.path_mode = path_mode
        self.tag = tag

    def matches(self, node_id: str, tags: Mapping[str, Set[str]] | None = None) -> PatternMatch | None:
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

        match = cls._compile_pattern(
            normalized_pattern, scope).match(normalized_value)
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
