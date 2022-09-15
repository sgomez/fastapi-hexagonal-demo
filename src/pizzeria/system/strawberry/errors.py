import strawberry


@strawberry.interface
class Error:
    """Error interface."""

    message: str
    code: str
    path: str


@strawberry.type
class ValidationError(Error):
    """Validation error interface."""


# _E = TypeVar("_E")


# class Context(Generic[_E]):
#     """Strawberry context."""

#     errors: List[_E] = []
#     success: bool = True


# class DomainErrorContext(AbstractContextManager["DomainErrorContext[_E]"], Generic[_E]):
#     errors: List[Union[_E, Error]] = []
#     success: bool = True

#     def __exit__(
#         self,
#         exc_type: Optional[Type[BaseException]],
#         exc_value: Optional[BaseException],
#         traceback: Optional[TracebackType],
#     ) -> Optional[bool]:
#         """Capture domain errors."""
#         match exc_value:
#             case errors.DomainError(message, label, code):
#                 self.success = False
#                 self.errors = [ValidationError(message=message, path=label, code=code)]
#             case _:
#                 return False

#         return True
