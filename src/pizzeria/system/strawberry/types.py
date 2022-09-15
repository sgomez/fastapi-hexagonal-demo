import base64
from dataclasses import asdict, dataclass
from typing import Any, TypeVar

import strawberry
from graphql import GraphQLError
from strawberry.fastapi import BaseContext

from ..bus import Command, MessageBus, Query


@dataclass
class Context(BaseContext):
    """Strawberry context."""

    command_bus: MessageBus[Command, None]
    query_bus: MessageBus[Query, Any]


SelfNode = TypeVar("SelfNode", bound="Node")


class Node:
    """Graphgql Node."""

    @classmethod
    def build_from_response(cls, obj: Any) -> SelfNode:
        """Build node from application layer response."""
        return cls(**(asdict(obj) | {"id": to_global_id(cls.__name__, str(obj.id))}))  # type: ignore

    @classmethod
    def build_from_input(cls, obj: Any) -> Any:
        """Builde node from graphql input."""
        return cls(**asdict(obj))


def to_global_id(node: str, id: str) -> strawberry.ID:
    """Return a string(node name) and an id converted to base64."""
    message = f"{node}:{id}"
    message_bytes = message.encode("utf-8")
    base64_bytes = base64.b64encode(message_bytes)
    return strawberry.ID(base64_bytes.decode("utf-8"))


def from_global_id(id: strawberry.ID | str) -> str:
    """Return an internal id."""
    base64_bytes = id.encode("utf-8")
    message_bytes = base64.b64decode(base64_bytes)
    try:
        return message_bytes.decode("utf-8").split(":")[1]
    except Exception as exc:
        raise GraphQLError("invalid_global_id") from exc
