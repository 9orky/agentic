#!/usr/bin/env python3
from __future__ import annotations

import ast
import json
import os
import re
import sys
from pathlib import Path


def normalize_pattern(value: str) -> str:
    return value.replace("\\", "/").strip().strip("/")


def compile_scope_pattern(pattern: str):
    normalized = normalize_pattern(pattern)
    regex = ["^"]
    index = 0

    while index < len(normalized):
        current = normalized[index]
        if current == "*":
            if index + 1 < len(normalized) and normalized[index + 1] == "*":
                regex.append("(.*)")
                index += 2
                continue
            regex.append("([^/]*)")
            index += 1
            continue
        if current == "?":
            regex.append("([^/])")
            index += 1
            continue

        regex.append(re.escape(current))
        index += 1

    regex.append("(?:/.*)?$")
    return re.compile("".join(regex))


def build_relative_import(path: Path, directory: Path, level: int, module: str | None, names: list[str]) -> list[str]:
    rel_dir = os.path.dirname(os.path.relpath(
        path, directory)).replace("\\", "/")
    parts = rel_dir.split("/") if rel_dir and rel_dir != "." else []
    if level > 1:
        parts = parts[: -(level - 1)]
    base = ".".join(parts) if parts else ""

    if module:
        return [f"{base}.{module}" if base else module]
    return [f"{base}.{name}" if base else name for name in names]


def count_python_files(directory: Path) -> int:
    total = 0
    for _, _, files_in_dir in os.walk(directory):
        total += sum(1 for file_name in files_in_dir if file_name.endswith(".py"))
    return total


def extract(directory: Path, exclusions: list[str]) -> dict[str, dict[str, list[str]]]:
    result: dict[str, dict[str, list[str]]] = {}
    files_found = 0
    files_excluded = 0
    compiled_exclusions = [compile_scope_pattern(
        pattern) for pattern in exclusions if normalize_pattern(pattern)]

    for root, dirs, files_in_dir in os.walk(directory):
        relative_root = Path(root).relative_to(directory)
        excluded_dirs = [
            name
            for name in dirs
            if any(pattern.match((relative_root / name).as_posix()) for pattern in compiled_exclusions)
        ]
        for name in excluded_dirs:
            excluded_count = count_python_files(Path(root) / name)
            files_found += excluded_count
            files_excluded += excluded_count
        dirs[:] = [name for name in dirs if name not in excluded_dirs]

        for file_name in files_in_dir:
            if not file_name.endswith(".py"):
                continue

            path = Path(root) / file_name
            relative_path = path.relative_to(directory).as_posix()
            files_found += 1
            if any(pattern.match(relative_path) for pattern in compiled_exclusions):
                files_excluded += 1
                continue

            try:
                content = path.read_text(encoding="utf-8")
                tree = ast.parse(content, filename=str(path))
            except (OSError, SyntaxError, UnicodeDecodeError):
                continue

            imports: list[str] = []
            classes: list[str] = []
            functions: list[str] = []

            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    imports.extend(alias.name for alias in node.names)
                elif isinstance(node, ast.ImportFrom):
                    if node.level > 0:
                        imports.extend(build_relative_import(
                            path, directory, node.level, node.module, [alias.name for alias in node.names]))
                    elif node.module:
                        imports.append(node.module)
                elif isinstance(node, ast.ClassDef):
                    classes.append(node.name)
                elif isinstance(node, ast.FunctionDef):
                    functions.append(node.name)

            result[relative_path] = {
                "imports": imports,
                "classes": classes,
                "functions": functions,
            }

    return {
        "files": result,
        "summary": {
            "files_found": files_found,
            "files_excluded": files_excluded,
            "files_checked": len(result),
        },
    }


def main() -> int:
    directory = Path(sys.argv[1]).resolve() if len(
        sys.argv) > 1 else Path.cwd()
    exclusions = json.loads(sys.argv[2]) if len(sys.argv) > 2 else []
    if not isinstance(exclusions, list):
        exclusions = []
    print(json.dumps(extract(directory, exclusions)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
