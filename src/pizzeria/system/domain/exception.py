from contextlib import AbstractContextManager
from dataclasses import dataclass
from typing import Dict, List


@dataclass(frozen=True)
class DomainError(Exception):
    message: str
    label: str
    code: str

    def __str__(self) -> str:
        """Allow returning a nice, human-readable representation of the model's instance."""
        return f"[{self.label}:{self.code}] {self.message}"

    def to_json(self) -> Dict[str, List[Dict[str, str]]]:
        """Allow returning a json representation of the model's instance."""
        return {self.label: [{"message": self.message, "code": self.code}]}


class LogicDomainError(DomainError):
    ...


class RuleDomainError(DomainError):
    ...


class DomainErrorContext(AbstractContextManager):
    errors: Dict[str, List[Dict[str, str]]] = {}
    success: bool = True

    def __exit__(self, exc_type, exc_value, traceback):
        """Capture domain errors."""
        if isinstance(exc_value, DomainError):
            self.success = False
            self.errors = exc_value.to_json()
            return True
