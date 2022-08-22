import strawberry
from strawberry import ID

from pizzeria.system.strawberry.types import Node


@strawberry.type
class PizzaNode(Node):
    id: ID
    name: str
    price: int
    toppings: list[str]


@strawberry.input
class PizzaInput:
    id: ID
    name: str
    price: int
    toppings: list[str]


@strawberry.type
class PizzaDuplicatedNameError:
    name: str
