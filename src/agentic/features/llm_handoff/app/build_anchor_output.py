from __future__ import annotations

from pathlib import Path

from ...architecture_check import ArchitectureSummary, describe_architecture
from ...configuration import ConfigLoadResult, load_config
from ...workspace_contract import WorkspaceContractSummary, describe_workspace_contract


def build_anchor_output(anchor_name: str, project_root: Path, explicit_config_path: str | None = None) -> str:
    if anchor_name == "bootstrap":
        return _build_bootstrap_anchor(describe_workspace_contract(project_root))
    if anchor_name == "rules":
        return _build_rules_anchor(describe_workspace_contract(project_root))
    if anchor_name == "config":
        return _build_config_anchor(load_config(project_root, explicit_config_path), project_root)
    if anchor_name == "architecture":
        return _build_architecture_anchor(describe_architecture(project_root, explicit_config_path), project_root)
    if anchor_name == "update":
        return _build_update_anchor(describe_workspace_contract(project_root))
    return _build_placeholder_anchor(anchor_name)


def _build_bootstrap_anchor(summary: WorkspaceContractSummary) -> str:
    lines = [
        "Anchor: bootstrap",
        "Command: agentic llm bootstrap",
        "Current collaboration surface:",
        f"- Local agentic directory: {_presence_label(summary.agentic_dir_exists)} ({_relative_path(summary.target_dir, summary.project_root)})",
        f"- Shared core rule docs present: {len(summary.shared_rule_paths)}/{len(summary.shared_rule_paths) + len(summary.missing_shared_rule_paths)}",
        f"- Config file: {_presence_label(summary.config_exists)} ({_relative_path(summary.config_path, summary.project_root)})",
        "Bootstrap behavior:",
        "- Run `agentic` to create or refresh the local collaboration surface.",
        "- Plain `agentic` is safe to rerun and preserves existing local files instead of overwriting them.",
        "- After bootstrap or refresh, rerun this anchor and `agentic llm rules` for current facts.",
    ]

    if summary.missing_shared_rule_paths:
        lines.append(
            f"- Missing shared rule docs: {_format_paths(summary.missing_shared_rule_paths, summary.project_root)}"
        )

    return "\n".join(lines)


def _build_rules_anchor(summary: WorkspaceContractSummary) -> str:
    lines = [
        "Anchor: rules",
        "Command: agentic llm rules",
        "Current rules surface:",
        f"- Shared core rule docs present: {len(summary.shared_rule_paths)}/{len(summary.shared_rule_paths) + len(summary.missing_shared_rule_paths)}",
        f"- Local override files: {len(summary.override_paths)}",
        f"- Local project-specific rule files: {len(summary.project_specific_paths)}",
        "Rule ownership:",
        "- Shared core docs are packaged rails and should not be edited in place.",
        "- Repo-local updates to an existing shared rule belong under `agentic/rules/overrides/`.",
        "- New repo-local rules belong under `agentic/rules/project-specific/`.",
    ]

    if summary.shared_rule_paths:
        lines.append(
            f"- Present shared rule docs: {_format_paths(summary.shared_rule_paths, summary.project_root)}"
        )
    if summary.missing_shared_rule_paths:
        lines.append(
            f"- Missing shared rule docs: {_format_paths(summary.missing_shared_rule_paths, summary.project_root)}"
        )
    if summary.override_paths:
        lines.append(
            f"- Override files: {_format_paths(summary.override_paths, summary.project_root)}"
        )
    if summary.project_specific_paths:
        lines.append(
            f"- Project-specific rule files: {_format_paths(summary.project_specific_paths, summary.project_root)}"
        )

    return "\n".join(lines)


def _build_update_anchor(summary: WorkspaceContractSummary) -> str:
    lines = [
        "Anchor: update",
        "Command: agentic llm update",
        "Current shared-rule state:",
        f"- Shared core rule docs present: {len(summary.shared_rule_paths)}/{len(summary.shared_rule_paths) + len(summary.missing_shared_rule_paths)}",
        f"- Config file currently present: {_presence_label(summary.config_exists)}",
        f"- Local override files present: {len(summary.override_paths)}",
        f"- Local project-specific rule files present: {len(summary.project_specific_paths)}",
        "Update behavior:",
        "- Run `agentic update` to refresh packaged shared rule docs.",
        "- `agentic update` overwrites shared core docs only.",
        "- `agentic update` preserves `agentic/agentic.yaml` and local rule files under overrides and project-specific.",
        "- After update, rerun the needed `agentic llm` anchors to recover fresh facts.",
    ]

    if summary.missing_shared_rule_paths:
        lines.append(
            f"- Shared docs that update would restore: {_format_paths(summary.missing_shared_rule_paths, summary.project_root)}"
        )

    return "\n".join(lines)


def _build_config_anchor(load_result: ConfigLoadResult, project_root: Path) -> str:
    boundaries = load_result.config.rules.boundaries
    lines = [
        "Anchor: config",
        "Command: agentic llm config",
        "Current configuration:",
        f"- Config path: {_relative_path(load_result.path, project_root)} ({load_result.source_format})",
        f"- Language: {load_result.config.language}",
        f"- Exclusion patterns: {len(load_result.config.exclusions)}",
        f"- Boundary rules: {len(boundaries)}",
    ]

    if load_result.config.exclusions:
        lines.append(
            f"- Exclusions: {', '.join(load_result.config.exclusions)}"
        )

    if boundaries:
        lines.append("Configured boundaries:")
        for index, boundary in enumerate(boundaries, start=1):
            disallow_text = ", ".join(
                boundary.disallow) if boundary.disallow else "none"
            allow_text = ", ".join(
                boundary.allow) if boundary.allow else "none"
            lines.append(
                f"- Rule {index}: source={boundary.source}; disallow={disallow_text}; allow={allow_text}; allow_same_match={str(boundary.allow_same_match).lower()}"
            )
    else:
        lines.append("- No boundary rules are configured yet.")

    lines.extend([
        "Config workflow:",
        "- Edit this config to change language, exclusions, or dependency boundaries.",
        "- After config changes, rerun `agentic llm config` and `agentic llm architecture`.",
        "- Run `agentic check` to validate the current config against repo structure.",
    ])

    return "\n".join(lines)


def _build_architecture_anchor(summary: ArchitectureSummary, project_root: Path) -> str:
    lines = [
        "Anchor: architecture",
        "Command: agentic llm architecture",
        "Current validation facts:",
        f"- Config path: {_relative_path(summary.config_path, project_root)} ({summary.config_format})",
        f"- Language: {summary.language}",
        f"- Required extractor runtime: {summary.runtime_command}",
    ]

    if summary.check_error is None:
        lines.extend([
            f"- Files found in scope: {summary.files_found}",
            f"- Files excluded by rules: {summary.files_excluded}",
            f"- Files checked: {summary.files_checked}",
            f"- Current boundary violations: {len(summary.violations)}",
        ])
        if summary.violations:
            for violation in summary.violations[:5]:
                lines.append(f"- Violation: {violation}")
            if len(summary.violations) > 5:
                lines.append(
                    "- Additional violations exist; run `agentic check` for the full list.")
    else:
        lines.append(
            f"- Current architecture facts unavailable: {summary.check_error}")

    lines.extend([
        "Validation workflow:",
        "- Run `agentic check` after meaningful config edits or code structure changes.",
        "- `agentic check` validates configured boundaries against normalized architecture facts keyed by repo-relative file path.",
        "- The normalized structure includes imports, classes, and functions for each file in scope.",
    ])

    if summary.check_error is not None:
        lines.append(
            "- Fix the reported runtime or extractor issue, then rerun `agentic check` and this anchor.")

    return "\n".join(lines)


def _build_placeholder_anchor(anchor_name: str) -> str:
    return (
        f"Anchor: {anchor_name}\n"
        f"Command: agentic llm {anchor_name}\n"
        "This anchor name is part of the stable agentic llm command contract.\n"
        f"Detailed {anchor_name} facts are not implemented yet.\n"
        "Use 'agentic llm' for the default handoff prompt."
    )


def _presence_label(value: bool) -> str:
    return "present" if value else "missing"


def _format_paths(paths: tuple[Path, ...] | list[Path], project_root: Path) -> str:
    return ", ".join(_relative_path(path, project_root) for path in paths)


def _relative_path(path: Path, project_root: Path) -> str:
    try:
        return path.relative_to(project_root).as_posix()
    except ValueError:
        return path.as_posix()
