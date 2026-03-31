from importlib import import_module

from .cli import ArchitectureCheckCli


def architecture_check_cli(app: object) -> None:
    register_architecture_check_cli = import_module(
        "agentic.features.architecture_check.policy_check"
    ).architecture_check_cli
    register_architecture_check_cli(app)


__all__ = ["ArchitectureCheckCli", "architecture_check_cli"]
