from typing import Any, Dict, Generic, Type, TypeVar

T = TypeVar("T")
R = TypeVar("R")


class Command:
    ...


class Query:
    ...


class Event:
    ...


class Handler(Generic[T, R]):
    async def handle(self, message: T) -> R:
        """Handle a message"""
        raise NotImplementedError


class MessageBus(Generic[T, R]):
    handlers: Dict[str, Handler[T, R]]

    def __init__(self) -> None:
        self.handlers = {}

    def register_handler(self, message: Type[T], handler: Handler) -> None:
        self.handlers[message.__name__] = handler

    async def dispatch(self, message: T) -> R:
        message_classname = message.__class__.__name__

        handler = self.handlers.get(message_classname)

        if not handler:
            raise RuntimeError(f"Handler not found for {message_classname}.")

        return await handler.handle(message)


query_bus = MessageBus[Query, Any]()
