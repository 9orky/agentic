from __future__ import annotations

from abc import ABC, abstractmethod

from .entity import RuleDocumentFile


class RuleDocumentRepository(ABC):
    @abstractmethod
    def find(self) -> tuple[RuleDocumentFile, ...]:
        raise NotImplementedError


__all__ = ["RuleDocumentRepository"]
