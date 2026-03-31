from .application import DescribeFileImportHotspotsQuery, FileImportHotspotEntry, FileImportHotspotsResult, build_default_describe_file_import_hotspots_query
from .ui import FileImportHotspotsView


def build_default_file_import_hotspots_view() -> FileImportHotspotsView:
    return FileImportHotspotsView()


__all__ = [
    "DescribeFileImportHotspotsQuery",
    "FileImportHotspotEntry",
    "FileImportHotspotsResult",
    "build_default_describe_file_import_hotspots_query",
    "build_default_file_import_hotspots_view",
]
