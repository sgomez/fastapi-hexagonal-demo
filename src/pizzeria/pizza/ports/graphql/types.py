import strawberry
from strawberry import ID

from pizzeria.system.strawberry.types import Node


@strawberry.type
class PizzaNode(Node):
    """Pizza node."""

    id: ID
    name: str
    price: int
    toppings: list[str]


@strawberry.input
class PizzaInput:
    """Pizza mutation input."""

    id: ID
    name: str
    price: int
    toppings: list[str]


@strawberry.type
class PizzaDuplicatedNameError:
    """Pizza mutation error."""

    name: str
