from .application import ArchitectureSummary, BuildArchitectureReportQuery, CheckResult, CheckerError, describe_architecture, run_architecture_check
from ..hotspots import build_default_describe_file_import_hotspots_query
from .application.queries.build_architecture_report import build_default_architecture_report_query
from .ui import ArchitectureCheckCli
from .ui.services import CheckSummaryPresenter
from .ui.views import GroupedViolationView, JsonReportView
from ..hotspots.ui import FileImportHotspotsView


def build_default_architecture_check_cli() -> ArchitectureCheckCli:
    return ArchitectureCheckCli(
        build_architecture_report_query=build_default_architecture_report_query(),
        describe_file_import_hotspots_query=build_default_describe_file_import_hotspots_query(),
        grouped_violation_view=GroupedViolationView(),
        file_import_hotspots_view=FileImportHotspotsView(),
        json_report_view=JsonReportView(),
        check_summary_presenter=CheckSummaryPresenter(),
    )


architecture_check_cli = build_default_architecture_check_cli().register

__all__ = [
    "ArchitectureCheckCli",
    "ArchitectureSummary",
    "BuildArchitectureReportQuery",
    "CheckResult",
    "CheckerError",
    "architecture_check_cli",
    "describe_architecture",
    "run_architecture_check",
]
