from dataclasses import dataclass
from typing import Dict, List


@dataclass(frozen=True)
class DomainError(Exception):
    """Base domain error."""

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
    """Business logic error."""


class RuleDomainError(DomainError):
    """Business rules error."""


class ValidationError(RuleDomainError):
    """Value object validation error."""
