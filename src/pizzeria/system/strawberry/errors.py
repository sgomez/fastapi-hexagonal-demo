from contextlib import AbstractContextManager
from typing import List

import strawberry

from pizzeria.system.domain import errors


@strawberry.interface
class Error:
    """Error interface."""

    message: str
    code: str
    path: str


@strawberry.type
class ValidationError(Error):
    """Validation error interface."""


class DomainErrorContext(AbstractContextManager):
    errors: List[Error] = []
    success: bool = True

    def __exit__(self, exc_type, exc_value, traceback):
        """Capture domain errors."""
        match exc_value:
            case errors.DomainError(message, label, code):
                self.success = False
                self.errors = [ValidationError(message=message, path=label, code=code)]
            case _:
                return False

        return True
