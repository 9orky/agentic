from __future__ import annotations

from enum import StrEnum


class SyncAction(StrEnum):
    CREATE = "create"
    UPDATE = "update"
    PRESERVE = "preserve"
    MISSING = "missing"
