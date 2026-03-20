from __future__ import annotations

from pathlib import Path

from ..contracts import AgenticConfigError


class LocalConfigPathResolver:
    def resolve(self, project_root: Path, explicit_config_path: str | None = None) -> Path | None:
        candidates: list[Path] = []
        if explicit_config_path:
            candidates.append(
                Path(explicit_config_path).expanduser().resolve())

        candidates.extend(
            [
                project_root / "agentic" / "agentic.yaml",
                project_root / "agentic" / "agentic.yml",
                project_root / "agentic.yaml",
                project_root / "agentic.yml",
            ]
        )

        seen: set[Path] = set()
        for candidate in candidates:
            normalized = candidate.resolve(strict=False)
            if normalized in seen:
                continue
            seen.add(normalized)
            if normalized.exists():
                return normalized
        return None


class LocalConfigTextReader:
    def read_text(self, path: Path) -> str:
        try:
            return path.read_text(encoding="utf-8")
        except OSError as exc:
            raise AgenticConfigError(
                f"Could not read config file: {path}") from exc
