from __future__ import annotations

from importlib.resources import as_file, files
from pathlib import Path
import json
import os
import shutil
import subprocess

from ...domain import CheckerError, ExtractionResult, ExtractorContractError
from ..extractor_registry import ExtractorSpec
from .extractor_runtime import ExtractorRuntime


class SubprocessExtractorRuntime(ExtractorRuntime):
    def run(self, spec: ExtractorSpec, project_root: Path, exclusions: list[str]) -> ExtractionResult:
        executable = self._resolve_extractor_command(spec.command)
        resource = files("agentic").joinpath(
            "resources", "arch", "extractors", spec.resource_name)
        with as_file(resource) as extractor_path:
            command = [executable, str(extractor_path), str(
                project_root), json.dumps(exclusions)]
            try:
                result = subprocess.run(
                    command, capture_output=True, text=True, check=True)
            except subprocess.CalledProcessError as exc:
                raise CheckerError(
                    exc.stderr.strip() or f"Extractor failed: {spec.resource_name}") from exc

        try:
            parsed = json.loads(result.stdout)
        except json.JSONDecodeError as exc:
            raise CheckerError(
                f"Extractor output was not valid JSON: {spec.resource_name}") from exc

        try:
            return ExtractionResult.validate_output(parsed, spec.resource_name)
        except ExtractorContractError as exc:
            raise CheckerError(str(exc)) from exc

    def _resolve_extractor_command(self, command_name: str) -> str:
        if os.path.sep in command_name or command_name.startswith("."):
            command_path = Path(command_name).expanduser()
            if command_path.exists():
                return str(command_path.resolve())
            raise CheckerError(
                f"Required runtime '{command_name}' is not available")

        executable = shutil.which(command_name)
        if executable is None:
            raise CheckerError(
                f"Required runtime '{command_name}' is not installed or not on PATH")
        return executable
