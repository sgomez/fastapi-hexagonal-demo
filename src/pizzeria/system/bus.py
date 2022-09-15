from typing import Any, Dict, Generic, Protocol, Type, TypeVar

from result import Result

from pizzeria.system.domain.errors import DomainError

T_contra = TypeVar("T_contra", contravariant=True)
R_co = TypeVar("R_co", covariant=True)


class Command:
    """Command base class."""

    ...


class Query:
    """Query base class."""

    ...


class Event:
    """Event base class."""

    ...


class Handler(Protocol[T_contra, R_co]):
    """Handler base class."""

    async def handle(self, message: T_contra) -> Result[R_co, list[DomainError]]:
        """Handle a message."""
        raise NotImplementedError


class MessageBus(Generic[T_contra, R_co]):
    """MessageBus base class."""

    handlers: Dict[str, Handler[T_contra, R_co]]

    def __init__(self) -> None:
        self.handlers = {}

    def register_handler(self, message: Type[T_contra], handler: Handler[T_contra, R_co]) -> None:
        """Add a handler."""
        self.handlers[message.__name__] = handler

    async def dispatch(self, message: T_contra) -> Result[R_co, list[DomainError]]:
        """Dispatch a message to the right handler."""
        message_classname = message.__class__.__name__

        handler = self.handlers.get(message_classname)

        if not handler:
            raise RuntimeError(f"Handler not found for {message_classname}.")

        return await handler.handle(message)


query_bus = MessageBus[Query, Any]()
