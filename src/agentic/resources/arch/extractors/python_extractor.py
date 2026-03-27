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


def collect_python_files(directory: Path, exclusions: list[str]) -> tuple[list[Path], int, int]:
    included_paths: list[Path] = []
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
            included_paths.append(path)

    return included_paths, files_found, files_excluded


def build_module_candidates(relative_path: str) -> list[str]:
    path = Path(relative_path)
    base_parts = list(path.parts)
    if not base_parts:
        return []

    if path.name == "__init__.py":
        base_parts = base_parts[:-1]
    else:
        base_parts = [*base_parts[:-1], path.stem]

    candidates: list[str] = []
    if base_parts:
        candidates.append(".".join(base_parts))
        if base_parts[0] == "src" and len(base_parts) > 1:
            candidates.append(".".join(base_parts[1:]))

    seen: set[str] = set()
    normalized: list[str] = []
    for candidate in candidates:
        if candidate and candidate not in seen:
            seen.add(candidate)
            normalized.append(candidate)
    return normalized


def preferred_module_name(relative_path: str) -> str:
    candidates = build_module_candidates(relative_path)
    for candidate in candidates:
        if not candidate.startswith("src."):
            return candidate
    return candidates[0] if candidates else ""


def build_module_index(paths: list[Path], directory: Path) -> dict[str, str]:
    module_index: dict[str, str] = {}
    for path in paths:
        relative_path = path.relative_to(directory).as_posix()
        for candidate in build_module_candidates(relative_path):
            module_index.setdefault(candidate, relative_path)
    return module_index


def resolve_relative_module_name(relative_path: str, level: int, module: str | None) -> str:
    current_module = preferred_module_name(relative_path)
    if not current_module:
        return module or ""

    if Path(relative_path).name == "__init__.py":
        package_parts = current_module.split(".")
    else:
        package_parts = current_module.split(".")[:-1]

    if level > 1:
        trim = level - 1
        package_parts = package_parts[:-
                                      trim] if trim <= len(package_parts) else []

    if module:
        package_parts.extend(part for part in module.split(".") if part)

    return ".".join(part for part in package_parts if part)


def resolve_import_targets(module_index: dict[str, str], module_name: str, imported_names: list[str]) -> list[str]:
    targets: list[str] = []

    if not imported_names:
        resolved_module = module_index.get(module_name, module_name)
        return [resolved_module] if resolved_module else []

    for imported_name in imported_names:
        if imported_name == "*":
            resolved_module = module_index.get(module_name, module_name)
            if resolved_module:
                targets.append(resolved_module)
            continue

        candidate_submodule = f"{module_name}.{imported_name}" if module_name else imported_name
        if candidate_submodule in module_index:
            targets.append(module_index[candidate_submodule])
            continue
        if module_name in module_index:
            targets.append(module_index[module_name])
            continue
        if module_name:
            targets.append(module_name)
            continue
        if candidate_submodule:
            targets.append(candidate_submodule)

    seen: set[str] = set()
    normalized: list[str] = []
    for target in targets:
        if target and target not in seen:
            seen.add(target)
            normalized.append(target)
    return normalized


def extract(directory: Path, exclusions: list[str]) -> dict[str, object]:
    result: dict[str, dict[str, list[str]]] = {}
    included_paths, files_found, files_excluded = collect_python_files(
        directory, exclusions)
    module_index = build_module_index(included_paths, directory)
    extraction_failures: list[str] = []

    for path in included_paths:
        relative_path = path.relative_to(directory).as_posix()

        try:
            content = path.read_text(encoding="utf-8")
            tree = ast.parse(content, filename=str(path))
        except (OSError, SyntaxError, UnicodeDecodeError) as exc:
            message = str(exc).strip()
            detail = f": {message}" if message else ""
            extraction_failures.append(
                f"{relative_path}: {exc.__class__.__name__}{detail}"
            )
            continue

        imports: list[str] = []
        classes: list[str] = []
        functions: list[str] = []

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(module_index.get(alias.name, alias.name))
            elif isinstance(node, ast.ImportFrom):
                imported_names = [alias.name for alias in node.names]
                if node.level > 0:
                    relative_module = resolve_relative_module_name(
                        relative_path,
                        node.level,
                        node.module,
                    )
                    imports.extend(
                        resolve_import_targets(
                            module_index,
                            relative_module,
                            imported_names,
                        )
                    )
                elif node.module:
                    imports.extend(
                        resolve_import_targets(
                            module_index,
                            node.module,
                            imported_names,
                        )
                    )
            elif isinstance(node, ast.ClassDef):
                classes.append(node.name)
            elif isinstance(node, ast.FunctionDef):
                functions.append(node.name)

        result[relative_path] = {
            "imports": imports,
            "classes": classes,
            "functions": functions,
        }

    if extraction_failures:
        raise RuntimeError(
            "Extractor failed to analyze Python files:\n"
            + "\n".join(extraction_failures)
        )

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
    try:
        print(json.dumps(extract(directory, exclusions)))
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
